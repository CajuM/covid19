#!/usr/bin/env python

import json
import tensorflow as tf

from covid19lib import convert_dfs
from covid19lib import get_dfs
from covid19lib import get_ds
from covid19lib import WINDOW_LEN

import autokeras as ak
import numpy as np

from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split


def main():
    deaths, recoveries, cases, deaths_validation, recoveries_validation, cases_validation = get_dfs()
    X, y = get_ds(deaths, recoveries, cases)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    data = convert_dfs(deaths_validation, recoveries_validation, cases_validation)

    column_names = []

    model_input = ak.Input()
    model_output = ak.blocks.basic.DenseBlock()(model_input)
    model_output = ak.blocks.basic.DenseBlock()(model_output)
    model_output = ak.blocks.basic.DenseBlock()(model_output)
    model_output = ak.RegressionHead()(model_output)

    trainer = ak.AutoModel(inputs=model_input, outputs=model_output)
    trainer.fit(X_train, y_train)

    model = trainer.export_model()
    y_fit = model.predict(X_test)

    tf.keras.models.save_model(model, 'model.tf')

    with open('data.json', 'wt') as f:
        json.dump(data, f)

    print(model.evaluate(X_test, y_test))

    plt.scatter(y_test, y_fit)
    plt.savefig('results.png')

if __name__ == '__main__':
    main()

