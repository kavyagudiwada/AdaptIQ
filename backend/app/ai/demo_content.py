"""Offline content bank used when the AI provider is unavailable (DEMO MODE).

Everything here is deterministic, curriculum-aware and genuinely
personalised (level + goal + weak topics are woven into the text), so the
product still demonstrates adaptation without an API key.
"""

from typing import Any

# --------------------------------------------------------------------------
# Initial assessment bank (topic: machine learning)
# key -> (question, [options], correct_index, subtopic, difficulty)
# --------------------------------------------------------------------------

ASSESSMENT_BANK: dict[str, list[dict[str, Any]]] = {
    "machine learning": [
        {
            "question": "Which Python library is primarily used for numerical computation on arrays?",
            "options": ["NumPy", "Pandas", "Matplotlib", "Flask"],
            "correct_index": 0,
            "subtopic": "NumPy",
            "difficulty": "easy",
        },
        {
            "question": "What does a DataFrame represent in Pandas?",
            "options": [
                "A 2D table of rows and columns",
                "A single numeric value",
                "A web server response",
                "A SQL query plan",
            ],
            "correct_index": 0,
            "subtopic": "Pandas",
            "difficulty": "easy",
        },
        {
            "question": "Handling missing values in a dataset is called what?",
            "options": [
                "Data preprocessing",
                "Model deployment",
                "Hyperparameter tuning",
                "Cross validation",
            ],
            "correct_index": 0,
            "subtopic": "Data preprocessing",
            "difficulty": "easy",
        },
        {
            "question": "Supervised learning uses which kind of data?",
            "options": [
                "Labelled data (input + correct output)",
                "Only unlabelled data",
                "Randomly generated data",
                "Images without captions",
            ],
            "correct_index": 0,
            "subtopic": "Supervised learning",
            "difficulty": "easy",
        },
        {
            "question": "Which task predicts a continuous numeric value?",
            "options": ["Regression", "Classification", "Clustering", "Dimensionality reduction"],
            "correct_index": 0,
            "subtopic": "Regression",
            "difficulty": "medium",
        },
        {
            "question": "K-Means is primarily used for which task?",
            "options": ["Classification", "Regression", "Clustering", "Dimensionality reduction"],
            "correct_index": 2,
            "subtopic": "Clustering",
            "difficulty": "medium",
        },
        {
            "question": "In K-Means, what does the parameter K represent?",
            "options": [
                "The number of clusters to form",
                "The learning rate",
                "The number of features",
                "The maximum depth of the tree",
            ],
            "correct_index": 0,
            "subtopic": "Clustering",
            "difficulty": "medium",
        },
        {
            "question": "Which metric is most appropriate for an imbalanced classification problem where the positive class matters?",
            "options": ["Accuracy", "Precision", "Log loss", "Mean squared error"],
            "correct_index": 1,
            "subtopic": "Model evaluation",
            "difficulty": "hard",
        },
        {
            "question": "What problem does regularisation primarily address?",
            "options": ["Overfitting", "Underfitting only", "Missing data", "Slow training"],
            "correct_index": 0,
            "subtopic": "Model evaluation",
            "difficulty": "medium",
        },
        {
            "question": "A model with very high training accuracy but poor test accuracy is most likely:",
            "options": ["Underfitting", "Overfitting", "Perfectly regularised", "Unbiased"],
            "correct_index": 1,
            "subtopic": "Model evaluation",
            "difficulty": "hard",
        },
    ],
}

# --------------------------------------------------------------------------
# Adaptive quiz bank: subtopic -> difficulty -> question
# --------------------------------------------------------------------------

QUIZ_BANK: dict[str, dict[str, list[dict[str, Any]]]] = {
    "regression": {
        "easy": [
            {
                "question": "What is the main goal of a regression model?",
                "options": [
                    "Predict a continuous numeric value",
                    "Assign a category label",
                    "Group similar items",
                    "Reduce feature count",
                ],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "easy",
                "explanation": "Regression predicts continuous numbers such as price, temperature or sales.",
            },
            {
                "question": "Which algorithm is a simple starting point for regression?",
                "options": ["Linear Regression", "K-Means", "PCA", "Naive Bayes"],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "easy",
                "explanation": "Linear Regression is the simplest supervised regression model and a great baseline.",
            },
        ],
        "medium": [
            {
                "question": "What does the slope coefficient in linear regression represent?",
                "options": [
                    "The change in prediction for a one-unit change in the feature",
                    "The average value of the target",
                    "The number of training rows",
                    "The model's confidence",
                ],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "medium",
                "explanation": "The slope is the expected change in the target per unit increase in that feature, holding others constant.",
            },
            {
                "question": "Why do we split data into training and test sets in regression?",
                "options": [
                    "To estimate performance on unseen data",
                    "To make training faster",
                    "To increase the dataset size",
                    "To remove outliers",
                ],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "medium",
                "explanation": "A held-out test set gives an honest estimate of generalisation rather than memorised training performance.",
            },
        ],
        "hard": [
            {
                "question": "A model shows low training error but high test error. Which regularisation approach most directly helps?",
                "options": [
                    "Add L1/L2 penalty to shrink coefficients",
                    "Increase the training set learning rate",
                    "Use more features",
                    "Remove the test set",
                ],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "hard",
                "explanation": "L1 (Lasso) and L2 (Ridge) penalties shrink coefficients, reducing variance and overfitting.",
            },
            {
                "question": "Which situation makes RMSE more informative than MAE?",
                "options": [
                    "When large errors must be penalised more heavily",
                    "When there are no errors",
                    "When the target is categorical",
                    "When the dataset is tiny",
                ],
                "correct_index": 0,
                "subtopic": "Regression",
                "difficulty": "hard",
                "explanation": "RMSE squares errors, so large misses dominate the score more than in MAE.",
            },
        ],
    },
    "classification": {
        "easy": [
            {
                "question": "What does a classifier output?",
                "options": [
                    "A discrete class label",
                    "A continuous price",
                    "A cluster centroid",
                    "A feature importance score",
                ],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "easy",
                "explanation": "Classification predicts discrete labels such as spam/not-spam or fraud/not-fraud.",
            },
            {
                "question": "Which is a common binary classification algorithm?",
                "options": ["Logistic Regression", "K-Means", "PCA", "t-SNE"],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "easy",
                "explanation": "Logistic Regression is a simple, strong baseline for binary classification.",
            },
        ],
        "medium": [
            {
                "question": "What is the decision threshold in Logistic Regression used for?",
                "options": [
                    "Converting predicted probability into a class label",
                    "Selecting the features",
                    "Splitting the dataset",
                    "Tuning the learning rate",
                ],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "medium",
                "explanation": "By default a 0.5 probability becomes the positive class; moving the threshold trades precision for recall.",
            },
            {
                "question": "Why can accuracy be misleading for a highly imbalanced dataset?",
                "options": [
                    "A model can score highly by always predicting the majority class",
                    "Accuracy cannot be computed",
                    "It always equals F1",
                    "It requires labels",
                ],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "medium",
                "explanation": "With 99% of one class, predicting that class always gives 99% accuracy while learning nothing.",
            },
        ],
        "hard": [
            {
                "question": "A fraud dataset is 1% positive. Which metric best reflects catching fraud?",
                "options": ["Recall (sensitivity)", "Accuracy", "Training time", "R-squared"],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "hard",
                "explanation": "Recall measures the share of actual fraud cases detected, which matters most when positives are rare.",
            },
            {
                "question": "What happens to precision if you lower the classification threshold?",
                "options": [
                    "Precision usually decreases and recall increases",
                    "Both increase",
                    "Both stay identical",
                    "The model stops training",
                ],
                "correct_index": 0,
                "subtopic": "Classification",
                "difficulty": "hard",
                "explanation": "Lowering the threshold flags more cases, so you catch more positives but also more false positives.",
            },
        ],
    },
    "clustering": {
        "easy": [
            {
                "question": "What is the goal of clustering?",
                "options": [
                    "Group similar data points without labels",
                    "Predict a known label",
                    "Estimate a continuous value",
                    "Evaluate model accuracy",
                ],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "easy",
                "explanation": "Clustering is unsupervised: it discovers structure in unlabelled data.",
            },
            {
                "question": "Which algorithm is unsupervised?",
                "options": ["K-Means", "Linear Regression", "Logistic Regression", "Gradient Boosting"],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "easy",
                "explanation": "K-Means needs no labels, while the others are supervised.",
            },
        ],
        "medium": [
            {
                "question": "What is the elbow method used for in K-Means?",
                "options": [
                    "Choosing a sensible value of K",
                    "Normalising features",
                    "Handling missing values",
                    "Splitting train and test data",
                ],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "medium",
                "explanation": "You plot inertia against K and pick the point where the curve flattens.",
            },
            {
                "question": "Why is feature scaling important before K-Means?",
                "options": [
                    "K-Means uses distances, so large-scale features dominate",
                    "K-Means cannot handle unscaled data at all",
                    "It increases the number of clusters",
                    "It labels the data automatically",
                ],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "medium",
                "explanation": "Distance-based methods are dominated by whichever feature has the largest numeric range.",
            },
        ],
        "hard": [
            {
                "question": "A K-Means result looks perfect on a 2D scatter plot but collapses on 1000 features. Most likely cause?",
                "options": [
                    "Features were not scaled, so a few large-range dimensions dominated the distance",
                    "K was set to 2",
                    "The data was labelled",
                    "Too many clusters were used",
                ],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "hard",
                "explanation": "In high dimensions unscaled features let a few dimensions control the distance, destroying cluster separation.",
            },
            {
                "question": "Which scenario makes K-Means perform poorly?",
                "options": [
                    "Non-globular cluster shapes such as concentric rings",
                    "Well-separated spherical clusters",
                    "Small, clean datasets",
                    "Standardised features",
                ],
                "correct_index": 0,
                "subtopic": "Clustering",
                "difficulty": "hard",
                "explanation": "K-Means assumes roughly spherical, similar-sized clusters, so ring-shaped data breaks that assumption.",
            },
        ],
    },
    "numpy": {
        "easy": [
            {
                "question": "What is a NumPy array compared to a Python list?",
                "options": [
                    "Faster, memory-efficient, supports vectorised operations",
                    "Slower but simpler",
                    "Only stores text",
                    "Cannot hold numbers",
                ],
                "correct_index": 0,
                "subtopic": "NumPy",
                "difficulty": "easy",
                "explanation": "NumPy stores homogeneous data in contiguous memory, enabling fast vectorised maths.",
            },
        ],
        "medium": [
            {
                "question": "What does NumPy broadcasting do?",
                "options": [
                    "Allows operations between arrays of different but compatible shapes",
                    "Copies data to a new database",
                    "Encrypts array values",
                    "Splits arrays into chunks",
                ],
                "correct_index": 0,
                "subtopic": "NumPy",
                "difficulty": "medium",
                "explanation": "Broadcasting stretches smaller arrays across larger ones so element-wise maths just works.",
            },
        ],
        "hard": [
            {
                "question": "Why can a Python loop over 10 million elements be far slower than NumPy vectorisation?",
                "options": [
                    "Loops run in the Python interpreter with per-element overhead, while NumPy runs compiled loops",
                    "Python cannot handle large lists",
                    "NumPy uses the GPU automatically",
                    "Loops drop floating point precision",
                ],
                "correct_index": 0,
                "subtopic": "NumPy",
                "difficulty": "hard",
                "explanation": "NumPy moves the loop into compiled C, avoiding interpreter overhead per element.",
            },
        ],
    },
    "pandas": {
        "easy": [
            {
                "question": "What is a Pandas Series?",
                "options": [
                    "A single labelled column of values",
                    "A SQL database",
                    "A plotting library",
                    "A neural network layer",
                ],
                "correct_index": 0,
                "subtopic": "Pandas",
                "difficulty": "easy",
                "explanation": "A Series is a labelled one-dimensional array; a DataFrame is a collection of Series.",
            },
        ],
        "medium": [
            {
                "question": "What does a Pandas merge do?",
                "options": [
                    "Combines two DataFrames using a common key",
                    "Deletes duplicate rows",
                    "Sorts by index only",
                    "Converts strings to numbers",
                ],
                "correct_index": 0,
                "subtopic": "Pandas",
                "difficulty": "medium",
                "explanation": "merge performs a SQL-like join on one or more shared columns.",
            },
        ],
        "hard": [
            {
                "question": "Your join silently produced more rows than either input table. What is the likely cause?",
                "options": [
                    "The join key has duplicate values, creating a many-to-many match",
                    "The index was reset",
                    "Columns were renamed",
                    "The data was sorted",
                ],
                "correct_index": 0,
                "subtopic": "Pandas",
                "difficulty": "hard",
                "explanation": "Duplicate keys on both sides multiply rows; use validate='m:1' to catch this early.",
            },
        ],
    },
    "data preprocessing": {
        "easy": [
            {
                "question": "Why do we scale features before training many models?",
                "options": [
                    "So no single large-scale feature dominates the model",
                    "To reduce the number of rows",
                    "To convert numbers to labels",
                    "To remove all duplicates",
                ],
                "correct_index": 0,
                "subtopic": "Data preprocessing",
                "difficulty": "easy",
                "explanation": "Scaling puts features on comparable ranges, which matters for distance- and gradient-based models.",
            },
        ],
        "medium": [
            {
                "question": "When should you fit a scaler on data?",
                "options": [
                    "Only on the training set, then apply the same transform to test data",
                    "On the full dataset to avoid bias",
                    "After training the model",
                    "Only on the test set",
                ],
                "correct_index": 0,
                "subtopic": "Data preprocessing",
                "difficulty": "medium",
                "explanation": "Fitting on all data leaks information from the test set and produces an optimistically biased score.",
            },
        ],
        "hard": [
            {
                "question": "Why must a target encoder be fitted inside a cross-validation fold?",
                "options": [
                    "Otherwise target statistics leak label information from validation rows into training",
                    "Because it is computationally expensive",
                    "Because it changes the target scale",
                    "Because encoders cannot handle categories",
                ],
                "correct_index": 0,
                "subtopic": "Data preprocessing",
                "difficulty": "hard",
                "explanation": "Out-of-fold encoding prevents the model from seeing validation labels when it builds target statistics.",
            },
        ],
    },
    "supervised learning": {
        "easy": [
            {
                "question": "What distinguishes supervised learning?",
                "options": [
                    "It trains on data with input-output pairs",
                    "It needs no data",
                    "It always uses images",
                    "It cannot be evaluated",
                ],
                "correct_index": 0,
                "subtopic": "Supervised learning",
                "difficulty": "easy",
                "explanation": "Supervised algorithms learn a mapping from labelled examples to predictions.",
            },
        ],
        "medium": [
            {
                "question": "What is a hyperparameter?",
                "options": [
                    "A setting chosen before training, such as learning rate or depth",
                    "A parameter learned from data",
                    "A target variable",
                    "A row in the dataset",
                ],
                "correct_index": 0,
                "subtopic": "Supervised learning",
                "difficulty": "medium",
                "explanation": "Hyperparameters are set by the developer and tuned via search, unlike learned model parameters.",
            },
        ],
        "hard": [
            {
                "question": "Why is cross-validation preferable to a single train/test split?",
                "options": [
                    "It uses every sample for both training and validation, giving a more stable estimate",
                    "It always yields a higher score",
                    "It removes the need for a test set ever",
                    "It avoids overfitting entirely",
                ],
                "correct_index": 0,
                "subtopic": "Supervised learning",
                "difficulty": "hard",
                "explanation": "Rotating folds reduces variance in the estimate and uses data far more efficiently.",
            },
        ],
    },
    "model evaluation": {
        "easy": [
            {
                "question": "What does a confusion matrix show?",
                "options": [
                    "Counts of correct and incorrect predictions per class",
                    "The list of features",
                    "Training loss over time",
                    "The learning rate schedule",
                ],
                "correct_index": 0,
                "subtopic": "Model evaluation",
                "difficulty": "easy",
                "explanation": "The matrix breaks predictions into true/false positives and negatives.",
            },
        ],
        "medium": [
            {
                "question": "What is overfitting?",
                "options": [
                    "The model learns training noise and performs poorly on new data",
                    "The model is too simple",
                    "Training failed to converge",
                    "The dataset is too large",
                ],
                "correct_index": 0,
                "subtopic": "Model evaluation",
                "difficulty": "medium",
                "explanation": "Overfitting shows as a gap between strong training performance and weak validation performance.",
            },
        ],
        "hard": [
            {
                "question": "You tuned 200 hyperparameter combinations and picked the best validation score. What is the risk?",
                "options": [
                    "You have overfit the validation set, so the reported score is optimistic",
                    "The test score must be identical",
                    "The model will underfit",
                    "Training data leaked into the model",
                ],
                "correct_index": 0,
                "subtopic": "Model evaluation",
                "difficulty": "hard",
                "explanation": "Repeated selection on the same validation set inflates the estimate; a nested or untouched test set is needed.",
            },
        ],
    },
    "decision trees": {
        "easy": [
            {
                "question": "What is a leaf node in a decision tree?",
                "options": [
                    "A node that outputs a prediction",
                    "The root of the tree",
                    "A feature name",
                    "A missing value",
                ],
                "correct_index": 0,
                "subtopic": "Decision Trees",
                "difficulty": "easy",
                "explanation": "Traversal ends at a leaf, which supplies the class or value prediction.",
            },
        ],
        "medium": [
            {
                "question": "What criterion do classification trees typically use to split nodes?",
                "options": [
                    "Reduction in impurity such as Gini or entropy",
                    "Mean squared error only",
                    "Random shuffling",
                    "Feature count",
                ],
                "correct_index": 0,
                "subtopic": "Decision Trees",
                "difficulty": "medium",
                "explanation": "The tree picks the split that most reduces impurity across the child nodes.",
            },
        ],
        "hard": [
            {
                "question": "Why are single decision trees often high variance?",
                "options": [
                    "Small changes in the data can produce a completely different tree structure",
                    "They cannot represent non-linear relationships",
                    "They ignore feature values",
                    "They always underfit",
                ],
                "correct_index": 0,
                "subtopic": "Decision Trees",
                "difficulty": "hard",
                "explanation": "Instability is exactly why bagging and boosting combine many trees to reduce variance.",
            },
        ],
    },
    "knn": {
        "easy": [
            {
                "question": "What does K in K-Nearest Neighbours represent?",
                "options": [
                    "How many nearby data points are consulted",
                    "The learning rate",
                    "The number of features",
                    "The cluster count",
                ],
                "correct_index": 0,
                "subtopic": "KNN",
                "difficulty": "easy",
                "explanation": "KNN classifies a point using the majority class of its K closest neighbours.",
            },
        ],
        "medium": [
            {
                "question": "Why is feature scaling critical for KNN?",
                "options": [
                    "KNN relies on distance, so unscaled features distort which points are near",
                    "KNN cannot handle numeric data",
                    "KNN needs labels to scale",
                    "Scaling changes the K value",
                ],
                "correct_index": 0,
                "subtopic": "KNN",
                "difficulty": "medium",
                "explanation": "A feature with range 10000 would otherwise dominate every distance calculation.",
            },
        ],
        "hard": [
            {
                "question": "KNN performs poorly on a dataset with many features. Why?",
                "options": [
                "Distances concentrate in high dimensions so all points look roughly equally far",
                "KNN requires a GPU",
                "KNN cannot use more than 100 rows",
                "KNN needs one-hot encoding",
            ],
            "correct_index": 0,
            "subtopic": "KNN",
            "difficulty": "hard",
            "explanation": "The curse of dimensionality makes distance-based methods lose discriminative power.",
            },
        ],
    },
    "ensemble methods": {
        "easy": [
            {
                "question": "What is the core idea behind Random Forest?",
                "options": [
                    "Combining many decision trees, each trained on different data and features",
                    "Using a single very deep tree",
                    "Clustering the features",
                    "Scaling the target variable",
                ],
                "correct_index": 0,
                "subtopic": "Ensemble methods",
                "difficulty": "easy",
                "explanation": "Averaging many decorrelated trees reduces variance dramatically.",
            },
        ],
        "medium": [
            {
                "question": "How does bagging differ from boosting?",
                "options": [
                    "Bagging trains trees in parallel on resampled data; boosting adds trees sequentially to fix errors",
                    "Bagging is supervised and boosting is not",
                    "Bagging uses more features and boosting uses fewer",
                    "They are identical techniques",
                ],
                "correct_index": 0,
                "subtopic": "Ensemble methods",
                "difficulty": "medium",
                "explanation": "Bagging reduces variance through averaging; boosting reduces bias by re-weighting errors.",
            },
        ],
        "hard": [
            {
                "question": "Why does boosting risk overfitting more than bagging?",
                "options": [
                    "Each new tree concentrates on the residual errors of earlier trees, including noise",
                    "Boosting trains fewer trees",
                    "Boosting cannot use probabilities",
                    "Bagging is always deterministic",
                ],
                "correct_index": 0,
                "subtopic": "Ensemble methods",
                "difficulty": "hard",
                "explanation": "Sequential error correction can chase label noise, so early stopping and shallow trees matter.",
            },
        ],
    },
    "python for ml": {
        "easy": [
            {
                "question": "Why do ML libraries use NumPy arrays instead of Python lists for numeric data?",
                "options": [
                    "Arrays store values in contiguous memory, which is far faster to process",
                    "Lists cannot store numbers at all",
                    "Arrays clean the data for you automatically",
                    "Lists only accept text values",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "easy",
                "explanation": "Contiguous memory and vectorised operations are why array libraries dominate numeric ML work.",
            },
            {
                "question": "What does train_test_split do in scikit-learn?",
                "options": [
                    "Divides your data into training and test sets",
                    "Removes duplicate rows",
                    "Converts text columns into numbers",
                    "Sorts the columns alphabetically",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "easy",
                "explanation": "The train/test separation is what lets you estimate generalisation honestly.",
            },
        ],
        "medium": [
            {
                "question": "How would you best describe a pandas DataFrame?",
                "options": [
                    "A 2D labelled table whose columns can hold different types",
                    "A single numeric value with an index",
                    "A plotting library",
                    "A database server",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "medium",
                "explanation": "Labelled rows and mixed-type columns make DataFrames the default input for ML data.",
            },
            {
                "question": "Why convert a pandas Series to a NumPy array before fitting a model?",
                "options": [
                    "Most estimators expect array-like numeric input rather than a labelled Series",
                    "Arrays always use less memory",
                    "A Series cannot be indexed",
                    "It converts category labels into numbers",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "medium",
                "explanation": "Estimators are strict about input type; .to_numpy() bridges the gap.",
            },
        ],
        "hard": [
            {
                "question": "What is the main reason to wrap preprocessing and the model in a Pipeline?",
                "options": [
                    "The same transforms are applied to training and validation folds, so preprocessing cannot leak",
                    "It always trains faster",
                    "It removes the need for cross-validation",
                    "It tunes every hyperparameter automatically",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "hard",
                "explanation": "Pipelines encapsulate steps so cross-validation never leaks preprocessing information.",
            },
            {
                "question": "Why can looping over DataFrame rows to train a model be so slow?",
                "options": [
                    "Row-at-a-time Python discards vectorised speed and pays per-row overhead",
                    "Loops are always numerically unstable",
                    "The model silently retrains each iteration",
                    "Memory is exhausted immediately",
                ],
                "correct_index": 0,
                "subtopic": "Python for ML",
                "difficulty": "hard",
                "explanation": "Batched vectorised operations are typically orders of magnitude faster than per-row iteration.",
            },
        ],
    },
    "feature engineering": {
        "easy": [
            {
                "question": "What is feature engineering?",
                "options": [
                    "Creating or transforming input columns so a model can learn better",
                    "Choosing which algorithm to use",
                    "Tuning the loss function",
                    "Deploying the model to production",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "easy",
                "explanation": "Feature quality usually matters more than the choice of algorithm.",
            },
            {
                "question": "What is one-hot encoding used for?",
                "options": [
                    "Turning categorical values into separate 0/1 columns",
                    "Scaling numbers between 0 and 1",
                    "Filling in missing values",
                    "Splitting data into folds",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "easy",
                "explanation": "It stops models from treating category labels as if they were ordered numbers.",
            },
        ],
        "medium": [
            {
                "question": "Why log-transform a heavily right-skewed feature such as income?",
                "options": [
                    "It compresses the long tail so the distribution is closer to the normal shape linear models assume",
                    "It deletes outliers permanently",
                    "It converts the column to text",
                    "It guarantees higher accuracy",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "medium",
                "explanation": "A log transform reduces skew and stabilises variance for linear assumptions.",
            },
            {
                "question": "A column that barely varies across the whole dataset is usually what?",
                "options": [
                    "Uninformative for the model and a candidate for removal",
                    "The single most important feature",
                    "Proof of target leakage",
                    "A sign of class imbalance",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "medium",
                "explanation": "A column that barely changes cannot help separate classes.",
            },
        ],
        "hard": [
            {
                "question": "What does target leakage look like during cross-validation?",
                "options": [
                    "An implausibly high validation score because the target influenced a feature",
                    "A model that never converges",
                    "Training and test sets with identical distributions",
                    "Training that takes much longer",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "hard",
                "explanation": "Leakage flatters validation scores and hides the real error you will meet in production.",
            },
            {
                "question": "Why can binning a continuous feature help a decision tree?",
                "options": [
                    "It reduces the number of thresholds the tree must search, limiting overfitting on noisy values",
                    "It introduces information that was not in the data",
                    "It guarantees the data becomes linearly separable",
                    "It removes the need for feature scaling",
                ],
                "correct_index": 0,
                "subtopic": "Feature engineering",
                "difficulty": "hard",
                "explanation": "Fewer candidate split points means a simpler tree that generalises better.",
            },
        ],
    },
    "model deployment": {
        "easy": [
            {
                "question": "What does a REST API let a trained model do?",
                "options": [
                    "Accept requests containing input data and return predictions",
                    "Train the model faster",
                    "Store raw data indefinitely",
                    "Remove the need for testing",
                ],
                "correct_index": 0,
                "subtopic": "Model deployment",
                "difficulty": "easy",
                "explanation": "The API is the contract that lets other applications call your model.",
            },
            {
                "question": "Why persist a trained model to a file such as .pkl?",
                "options": [
                    "So the exact trained state reloads later and produces identical predictions",
                    "To compress the dataset",
                    "To share the training code",
                    "To encrypt the feature values",
                ],
                "correct_index": 0,
                "subtopic": "Model deployment",
                "difficulty": "easy",
                "explanation": "Serialising the model avoids retraining and guarantees consistent outputs.",
            },
        ],
        "medium": [
            {
                "question": "Why keep a validation set separate from the test set?",
                "options": [
                    "To choose and tune the model without contaminating the final test estimate",
                    "To increase the amount of training data",
                    "To replace cross-validation entirely",
                    "To remove the need for a test set",
                ],
                "correct_index": 0,
                "subtopic": "Model deployment",
                "difficulty": "medium",
                "explanation": "The test set must stay untouched until the one final evaluation.",
            },
            {
                "question": "What usually causes high training accuracy but much lower validation accuracy?",
                "options": [
                    "Overfitting to the training data",
                    "Using too little data at training time only",
                    "A correct, leak-free preprocessing pipeline",
                    "Stratified splitting",
                ],
                "correct_index": 0,
                "subtopic": "Model deployment",
                "difficulty": "medium",
                "explanation": "High train and low validation is the classic overfitting signature.",
            },
        ],
        "hard": [
            {
                "question": "A model scores well offline but poorly in production. Which cause is least likely?",
                "options": [
                    "Feature skew between training data and live traffic",
                    "Train/validation/test split leakage",
                    "Distribution shift in production inputs",
                    "Missing monitoring and drift detection",
                ],
                "correct_index": 1,
                "subtopic": "Model deployment",
                "difficulty": "hard",
                "explanation": "Leakage flatters offline scores; skew, drift and missing monitoring cause production drops.",
            },
            {
                "question": "Why prefer a shadow deployment over an immediate full release?",
                "options": [
                    "It produces predictions on real traffic without serving them to users, so you can compare safely first",
                    "It removes the need for monitoring",
                    "It retrains the model every hour",
                    "It guarantees zero latency",
                ],
                "correct_index": 0,
                "subtopic": "Model deployment",
                "difficulty": "hard",
                "explanation": "Shadowing de-risks a release by validating against the live distribution first.",
            },
        ],
    },
}

# Generic bank so unknown topics still produce sensible questions in demo mode.
GENERIC_QUIZ_BANK: dict[str, list[dict[str, Any]]] = {
    "easy": [
        {
            "question": "Which statement best describes the core idea of this topic?",
            "options": [
                "It provides a structured way to solve a defined class of problems",
                "It applies only to large datasets",
                "It requires no prior knowledge",
                "It always produces a single correct output",
            ],
            "correct_index": 0,
            "subtopic": "Core concepts",
            "difficulty": "easy",
            "explanation": "Start with the definition and one concrete example, then build the vocabulary around it.",
        },
        {
            "question": "What should you understand first when learning this topic?",
            "options": [
                "The key terminology and definitions",
                "Advanced edge cases",
                "Performance optimisation",
                "Deployment pipelines",
            ],
            "correct_index": 0,
            "subtopic": "Key terminology",
            "difficulty": "easy",
            "explanation": "Vocabulary is the foundation; without it, later material is hard to follow.",
        },
    ],
    "medium": [
        {
            "question": "Why is it useful to practise a topic on a small real example?",
            "options": [
                "It connects abstract ideas to something concrete you can verify",
                "It replaces reading the theory",
                "It guarantees correct answers",
                "It is only needed for exams",
            ],
            "correct_index": 0,
            "subtopic": "Practical application",
            "difficulty": "medium",
            "explanation": "Working examples make the mental model concrete and reveal where your understanding breaks.",
        },
        {
            "question": "What is the best way to check whether you truly understand a concept?",
            "options": [
                "Explain it in your own words and apply it to a new problem",
                "Re-read the same paragraph",
                "Memorise the definition verbatim",
                "Highlight it in your notes",
            ],
            "correct_index": 0,
            "subtopic": "Best practices",
            "difficulty": "medium",
            "explanation": "Recall plus application is a much stronger signal of understanding than recognition.",
        },
    ],
    "hard": [
        {
            "question": "A worked example works but a new scenario fails. What is the most likely gap?",
            "options": [
                "You memorised the example rather than the underlying principle",
                "You did not read enough articles",
                "The scenario is invalid",
                "You need a larger dataset",
            ],
            "correct_index": 0,
            "subtopic": "Real-world case study",
            "difficulty": "hard",
            "explanation": "Transfer requires the principle, not the specific instance - that is the key advanced skill.",
        },
        {
            "question": "How would you verify a solution to an unfamiliar problem in this area?",
            "options": [
                "Test it against known cases and check edge conditions",
                "Assume the first plausible answer is right",
                "Skip verification entirely",
                "Only check that it runs",
            ],
            "correct_index": 0,
            "subtopic": "Practice problems",
            "difficulty": "hard",
            "explanation": "Verification against known cases plus edge conditions separates real mastery from guesswork.",
        },
    ],
}
