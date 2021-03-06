# -*- encoding: utf-8 -*-
from autosklearn.evaluation.abstract_evaluator import AbstractEvaluator
from autosklearn.evaluation.util import calculate_score


__all__ = [
    'TestEvaluator'
]


class TestEvaluator(AbstractEvaluator):

    def __init__(self, Datamanager, output_dir,
                 configuration=None,
                 with_predictions=False,
                 all_scoring_functions=False,
                 seed=1):
        super(TestEvaluator, self).__init__(
            Datamanager, output_dir, configuration,
            with_predictions=with_predictions,
            all_scoring_functions=all_scoring_functions,
            seed=seed,
            output_y_test=False,
            num_run='dummy')
        self.configuration = configuration

        self.X_train = Datamanager.data['X_train']
        self.Y_train = Datamanager.data['Y_train']

        self.X_test = Datamanager.data.get('X_test')
        self.Y_test = Datamanager.data.get('Y_test')

    def fit(self):
        self.model.fit(self.X_train, self.Y_train)

    # override
    def predict(self, train=False):

        if train:
            Y_pred = self.predict_function(self.X_train, self.model,
                                           self.task_type, self.Y_train)
            score = calculate_score(
                solution=self.Y_train,
                prediction=Y_pred,
                task_type=self.task_type,
                metric=self.metric,
                num_classes=self.D.info['label_num'],
                all_scoring_functions=self.all_scoring_functions)
        else:
            Y_pred = self.predict_function(self.X_test, self.model,
                                           self.task_type, self.Y_train)
            score = calculate_score(
                solution=self.Y_test,
                prediction=Y_pred,
                task_type=self.task_type,
                metric=self.metric,
                num_classes=self.D.info['label_num'],
                all_scoring_functions=self.all_scoring_functions)

        if hasattr(score, '__len__'):
            err = {key: 1 - score[key] for key in score}
        else:
            err = 1 - score

        if self.with_predictions:
            return err, Y_pred, Y_pred, Y_pred
        return err
