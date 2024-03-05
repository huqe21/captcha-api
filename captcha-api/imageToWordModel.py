import cv2
import os
import stow
import onnxruntime as ort
import typing
import numpy as np
from itertools import groupby



class ImageToWordModel():
    def __init__(self, char_list: typing.Union[str, list], model_path: str = "", force_cpu: bool = False, default_model_name: str = "model.onnx", *args, **kwargs):
        self.char_list = char_list
        self.model_path = model_path
        self.force_cpu = force_cpu
        self.default_model_name = default_model_name

        if isinstance(stow.artefact(self.model_path), stow.Directory):
            self.model_path = stow.join(self.model_path, self.default_model_name)

        if not os.path.exists(self.model_path):
            raise Exception(f"Model path ({self.model_path}) does not exist")

        providers = ['CUDAExecutionProvider'] if ort.get_device() == "GPU" and not force_cpu else [
            'CPUExecutionProvider']

        self.model = ort.InferenceSession(self.model_path, providers=providers)
        self.input_shape = self.model.get_inputs()[0].shape[1:]
        self.input_name = self.model._inputs_meta[0].name
        self.output_name = self.model._outputs_meta[0].name

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])

        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(None, {self.input_name: image_pred})[0]

        text = self.ctc_decoder(preds, self.char_list)[0]

        return text

    def ctc_decoder(self, predictions: np.ndarray, chars: typing.Union[str, list]) -> typing.List[str]:
        ''' CTC greedy decoder for predictions

        Args:
            predictions (np.ndarray): predictions from model
            chars (typing.Union[str, list]): list of characters

        Returns:
            typing.List[str]: list of words
        '''
        # use argmax to find the index of the highest probability
        argmax_preds = np.argmax(predictions, axis=-1)

        # use groupby to find continuous same indexes
        grouped_preds = [[k for k, _ in groupby(preds)] for preds in argmax_preds]

        # convert indexes to chars
        texts = ["".join([chars[k] for k in group if k < len(chars)]) for group in grouped_preds]

        return texts

    def get_cer(self, preds: typing.Union[str, typing.List[str]], target: typing.Union[str, typing.List[str]]):
        """ Update the cer score with the current set of references and predictions.

        Args:
            preds (typing.Union[str, typing.List[str]]): list of predicted words
            target (typing.Union[str, typing.List[str]]): list of target words

        Returns:
            Character error rate score
        """
        if isinstance(preds, str):
            preds = [preds]
        if isinstance(target, str):
            target = [target]

        total, errors = 0, 0
        for pred_tokens, tgt_tokens in zip(preds, target):
            errors += self.edit_distance(list(pred_tokens), list(tgt_tokens))
            total += len(tgt_tokens)

        cer = errors / total
        return cer

    def edit_distance(self, prediction_tokens: typing.List[str], reference_tokens: typing.List[str]) -> int:
        """ Standard dynamic programming algorithm to compute the Levenshtein Edit Distance Algorithm
        Args:
            prediction_tokens: A tokenized predicted sentence
            reference_tokens: A tokenized reference sentence
        Returns:
            Edit distance between the predicted sentence and the reference sentence
        """
        dp = [[0] * (len(reference_tokens) + 1) for _ in range(len(prediction_tokens) + 1)]
        for i in range(len(prediction_tokens) + 1):
            dp[i][0] = i

        dp[0] = [j for j in range(len(reference_tokens) + 1)]

        for i, p_tok in enumerate(prediction_tokens):
            for j, r_tok in enumerate(reference_tokens):
                if p_tok == r_tok:
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = min(dp[i][j + 1], dp[i + 1][j], dp[i][j]) + 1

        return dp[-1][-1]

    def __call__(self, image: np.ndarray):
        return self.predict(image)