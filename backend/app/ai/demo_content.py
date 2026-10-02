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

# --------------------------------------------------------------------------
# Tutor bank: subtopic -> topic-specific explanation + worked example problem.
# Each entry answers a real, precise question about the subtopic and includes a
# concrete numeric problem solved step by step, so every topic reads distinctly
# even in offline mode. Formulas use LaTeX delimiters ($...$ / $$...$$) so the
# frontend renders them as readable maths.
# --------------------------------------------------------------------------

TUTOR_BANK: dict[str, dict[str, Any]] = {
    "regression": {
        "explanation": (
            "**Regression** predicts a continuous number from input features. "
            "You are fitting a line (or surface) $y \\approx f(x)$ by choosing parameters that "
            "minimise how wrong the predictions are. For a simple linear model "
            "$y = \\beta_0 + \\beta_1 x + \\varepsilon$, the ordinary least squares solution is\n\n"
            "$$\\hat{\\beta}_1 = \\frac{\\text{cov}(x, y)}{\\text{var}(x)}, \\quad "
            "\\hat{\\beta}_0 = \\bar{y} - \\hat{\\beta}_1 \\bar{x}$$\n\n"
            "where $\\hat{\\beta}_1$ is the slope (change in $y$ per unit change in $x$) and "
            "$\\hat{\\beta}_0$ the intercept. In practical libraries this is embedded as "
            "$\\hat{\\beta} = (X^T X)^{-1} X^T y$, the normal equations, which only require that "
            "$X^T X$ be invertible — so the first thing to check before fitting is highly "
            "correlated (collinear) features.\n\n"
            "The result is a line that minimises the mean squared error "
            "$\\text{MSE} = \\frac{1}{n}\\sum_i (y_i - \\hat{y}_i)^2$, and the coefficient of "
            "determination $R^2 = 1 - \\text{MSE}/\\text{var}(y)$ tells you the fraction of "
            "variance your features explain."
        ),
        "example": (
            "**Worked problem.** Predict house price $y$ (in lakhs) from size $x$ (in sq ft). "
            "Three houses: $(600, 30)$, $(800, 38)$, $(1000, 46)$.\n\n"
            "**Step 1 — means.** $\\bar{x} = (600+800+1000)/3 = 800$, $\\bar{y} = (30+38+46)/3 = 38$.\n"
            "**Step 2 — slope.** "
            "$\\hat{\\beta}_1 = \\frac{(600-800)(30-38)+(800-800)(38-38)+(1000-800)(46-38)}\n"
            "{(600-800)^2+(800-800)^2+(1000-800)^2} = \\frac{(-200)(-8)+(0)(0)+(200)(8)}{40000+0+40000} = \\frac{3200}{80000} = 0.04$.\n"
            "**Step 3 — intercept.** $\\hat{\\beta}_0 = 38 - 0.04(800) = 38 - 32 = 6$.\n"
            "**Step 4 — model.** $\\hat{y} = 6 + 0.04x$. A 900 sq ft house predicts $6 + 0.04(900) = 42$ lakhs.\n"
            "**Step 5 — residual.** The interpretation: each extra 100 sq ft adds about $\\$0.04 \\times 100 = 4$ lakhs."
        ),
        "key_points": [
            "Predicts a continuous target, not a category.",
            "OLS minimises squared residuals; slope is covariance over variance.",
            "$R^2$ measures how much target variance the features explain.",
            "Check collinearity before trusting the normal equations.",
        ],
        "common_mistakes": [
            "Reading $R^2$ as a guarantee of causation rather than fit.",
            "Fitting before removing highly correlated predictors, which inverts $X^TX$.",
        ],
        "follow_up_question": "If two features are perfectly correlated, why does $(X^TX)^{-1}$ fail, and what does ridge regression change?",
    },
    "classification": {
        "explanation": (
            "**Classification** assigns each example to one of a fixed set of discrete classes. "
            "Instead of fitting a line to a number, you learn a decision boundary "
            "$f(x) = \\text{sign}(w \\cdot x + b)$ that separates the classes. Logistic regression "
            "softens this boundary into a probability using the sigmoid\n\n"
            "$$\\sigma(z) = \\frac{1}{1 + e^{-z}}, \\quad z = w \\cdot x + b$$\n\n"
            "so $P(y=1 \\mid x) = \\sigma(z)$; a datum is classified as class 1 when "
            "$\\sigma(z) \\geq 0.5$. The parameters $w, b$ are chosen by maximising the log-likelihood of "
            "the labels (equivalent to minimising cross-entropy), which is a convex problem solvable by "
            "gradient descent.\n\n"
            "Two practical notes: the boundary is a straight hyperplane in the *feature* space, so "
            "non-linearly separable data needs engineered or kernel features; and when classes are "
            "imbalanced, accuracy is a trap — precision and recall matter more."
        ),
        "example": (
            "**Worked problem.** Predict whether an email is spam (1) or not (0) using one feature "
            "$x$ = number of exclamation marks. Suppose you fit $w = 0.4$, $b = -2$, so "
            "$z = 0.4x - 2$ and $P(\\text{spam}) = 1/(1+e^{-z})$.\n\n"
            "**Step 1.** For $x = 3$: $z = 0.4(3) - 2 = -0.8$. "
            "$\\sigma(-0.8) = 1/(1+e^{0.8}) \\approx 1/(1+2.225) \\approx 0.31$.\n"
            "**Step 2.** Since $0.31 < 0.5$, the email is predicted **not spam**.\n"
            "**Step 3.** For $x = 8$: $z = 0.4(8)-2 = 1.2$. $\\sigma(1.2) \\approx 1/(1+e^{-1.2}) \\approx 0.77$.\n"
            "**Step 4.** Since $0.77 \\geq 0.5$, predicted **spam**.\n"
            "**Step 5.** The boundary is where $z=0$, i.e. $x = b/|w| = 2/0.4 = 5$ — the cutoff "
            "between the two classes."
        ),
        "key_points": [
            "Outputs a probability via the sigmoid $\\sigma(w \\cdot x + b)$.",
            "A threshold of 0.5 defines the linear decision boundary.",
            "Parameters come from maximising label likelihood (cross-entropy).",
            "Use precision/recall, not accuracy, on imbalanced classes.",
        ],
        "common_mistakes": [
            "Reporting accuracy on a dataset where one class is 95% of the data.",
            "Treating the raw sigmoid probability without calibrating the threshold for cost.",
        ],
        "follow_up_question": "Where does the 0.5 threshold come from, and how would you move it to reduce false negatives on spam?",
    },
    "clustering": {
        "explanation": (
            "**Clustering** finds groups in data when there are no labels. K-Means partitions $n$ points "
            "into $k$ clusters by minimising the within-cluster sum of squares\n\n"
            "$$\\text{WCSS} = \\sum_{j=1}^{k}\\sum_{x \\in C_j} \\|x - \\mu_j\\|^2$$\n\n"
            "where $\\mu_j$ is the centroid of cluster $C_j$. The algorithm alternates two steps: "
            "(1) **assign** every point to the nearest centroid, and (2) **update** each centroid to "
            "the mean of its assigned points, repeating until assignments stop changing.\n\n"
            "Because convergence lands in a local minimum, you run it several times from different "
            "seeds and keep the lowest WCSS. The choice of $k$ is genuinely ambiguous — the elbow "
            "method plots WCSS against $k$ and looks for the point where adding another cluster "
            "stops buying much."
        ),
        "example": (
            "**Worked problem.** Cluster four points $A(0,0)$, $B(1,0)$, $C(8,8)$, $D(9,9)$ with "
            "$k=2$, initial centroids $\\mu_1=(0,0)$, $\\mu_2=(8,8)$.\n\n"
            "**Step 1 — assign.** "
            "$d(A,\\mu_1)=0$, $d(A,\\mu_2)=\\sqrt{128}\\approx 11.3$ → $A \\in C_1$.\n"
            "$d(B,\\mu_1)=1$, $d(B,\\mu_2)=\\sqrt{(7)^2+(8)^2}=\\sqrt{113}$ → $B \\in C_1$.\n"
            "$d(C,\\mu_1) \\approx 11.3$, $d(C,\\mu_2)=0$ → $C \\in C_2$.\n"
            "$d(D,\\mu_1) \\approx 12.7$, $d(D,\\mu_2) \\approx 1.4$ → $D \\in C_2$.\n"
            "**Step 2 — update centroids.** $\\mu_1 = ((0+1)/2,\\, (0+0)/2) = (0.5, 0)$, "
            "$\\mu_2 = ((8+9)/2,\\, (8+9)/2) = (8.5, 8.5)$.\n"
            "**Step 3 — reassign.** New distances keep all four points in the same clusters (verify: "
            "$B$ is closer to $(0.5,0)$ than to $(8.5,8.5)$), so the assignment is stable. "
            "Final: $C_1 = \\{A,B\\}$, $C_2 = \\{C,D\\}$ with WCSS $(0.5^2+0.5^2)+(0.5^2+0.5^2)=1+1=2$."
        ),
        "key_points": [
            "K-Means minimises within-cluster squared distance to centroids.",
            "Iterate assign-then-update until the assignment is stable.",
            "Converges locally — restart with multiple seeds, keep lowest WCSS.",
            "Pick $k$ with the elbow method or domain knowledge.",
        ],
        "common_mistakes": [
            "Choosing $k$ by eye without the elbow plot or a task requirement.",
            "Applying K-Means to raw data with wildly different feature scales.",
        ],
        "follow_up_question": "Why does standardising features change what K-Means discovers, and when would you still keep raw units?",
    },
    "numpy": {
        "explanation": (
            "**NumPy** is Python's array library; nearly every ML package is built on its `ndarray`. "
            "The key idea is **vectorisation**: you express operations over whole arrays rather than "
            "looping in Python, which moves the loop into compiled C. Core routines such as "
            "$(x - \\mu) / \\sigma$ act elementwise, and every element of a `(m, n)` array carries a "
            "`dtype` so it stays compact in memory.\n\n"
            "Broadcasting lets two arrays with different shapes combine if their dimensions are "
            "compatible from the *right* edge: a `(3, 1)` column and a `(1, 4)` row produce a "
            "`(3, 4)` result. This is what makes normalisation, distance matrices and matrix "
            "multiplication (`dot`) natural one-liners instead of triply-nested loops."
        ),
        "example": (
            "**Worked problem.** Standardise an array (z-score) so each feature has mean 0 and "
            "variance 1, using broadcasting.\n\n"
            "```python\n"
            "import numpy as np\n"
            "X = np.array([[200.0, 35.0],\n"
            "              [300.0, 45.0],\n"
            "              [100.0, 40.0]])   # shape (3, 2): 3 samples, 2 features\n"
            "mu    = X.mean(axis=0)           # array([200., 40.])\n"
            "sigma = X.std(axis=0)            # array([81.64965809, 4.0824829 ])\n"
            "Z = (X - mu) / sigma             # broadcasts (3,2)-(1,2)=>(3,2)\n"
            "print(Z.round(2))\n"
            "# [[ 0.   -1.22]\n"
            "#  [ 1.22  1.22]\n"
            "#  [-1.22  0.  ]]\n"
            "print(Z.mean(axis=0).round(6), Z.std(axis=0).round(6))\n"
            "# [0. 0.]  [1. 1.]\n"
            "```\n"
            "If you tried this with Python lists, you would need a nested loop per feature; "
            "the vector form is one expression and runs in compiled code."
        ),
        "key_points": [
            "`ndarray` is a homogeneous, typed, multi-dimensional array.",
            "Vectorise with elementwise ops instead of Python loops.",
            "Broadcasting aligns trailing axes; a `(3,1)` with a `(1,4)` gives `(3,4)`.",
            "Use `mean/std` along `axis=0` for per-feature statistics.",
        ],
        "common_mistakes": [
            "Forgetting `axis=` and getting the global mean instead of a per-column one.",
            "Using Python loops over array elements, which destroys NumPy's speed advantage.",
        ],
        "follow_up_question": "What is the difference between `numpy.dot`, `@`, and elementwise `*` on a pair of 2-D arrays?",
    },
    "pandas": {
        "explanation": (
            "**Pandas** provides the `DataFrame`: a labelled, 2-D table of rows (samples) and "
            "columns (features). Its power is the split-apply-combine pattern: `groupby` splits rows "
            "by a key, you apply a function to each group, and the results come back aligned by index. "
            "This is the backbone of tabular feature engineering.\n\n"
            "Merging/`join` brings different tables together on shared keys (SQL-style), and because "
            "column operations are vectorised, transformations like `df['x'] - df['x'].mean()` apply to "
            "every row at once. Missing values are represented as `NaN`; `dropna` removes rows and "
            "`fillna` imputes, but which one is safe always depends on the meaning of the missingness."
        ),
        "example": (
            "**Worked problem.** Compute the mean house price per city, then attach that average back "
            "to every row as a new feature (a common aggregation pattern).\n\n"
            "```python\n"
            "import pandas as pd\n"
            "df = pd.DataFrame({\n"
            "    'city': ['A', 'B', 'A', 'B', 'A'],\n"
            "    'price': [30, 38, 46, 50, 34],\n"
            "})\n"
            "city_mean = df.groupby('city')['price'].mean()\n"
            "print(city_mean)\n"
            "# city\n"
            "# A    36.666667\n"
            "# B    44.000000\n"
            "df['city_price_mean'] = df['city'].map(city_mean)   # align key back to rows\n"
            "print(df)\n"
            "#   city  price  city_price_mean\n"
            "# 0    A     30              36.666667\n"
            "# 1    B     38              44.000000\n"
            "# 2    A     46              36.666667\n"
            "# 3    B     50              44.000000\n"
            "# 4    A     34              36.666667\n"
            "```\n"
            "The `map` step is the 'combine' — the per-city mean becomes a per-row column."
        ),
        "key_points": [
            "`DataFrame` = labelled rows/columns with vectorised column ops.",
            "`groupby` → split, apply function, combine back via index/map.",
            "Merging joins tables on shared keys, SQL-style.",
            "`NaN` handling (`dropna`/`fillna`) must respect why data is missing.",
        ],
        "common_mistakes": [
            "`groupby` without selecting the column, then expecting a tidy Series.",
            "Merging on columns with different dtypes or names, silently producing NaN matches.",
        ],
        "follow_up_question": "Why does `groupby('city').mean()` drop non-numeric columns while `agg` keeps control of which columns to reduce?",
    },
    "data preprocessing": {
        "explanation": (
            "**Data preprocessing** turns raw data into the matrix a model can learn from. The three "
            "moves are: **handle missing values** (drop rows, impute mean/median), **scale features** "
            "so one variable does not dominate the distance or gradient, and **encode categories** "
            "into numbers. The single most important rule is that every statistic you compute — the "
            "imputation mean, the scaler $\\mu, \\sigma$, the encoding vocabulary — must be fitted on "
            "the **training** split only, then applied to the test split with the same numbers.\n\n"
            "Standardisation scales to zero mean and unit variance, "
            "$z = (x-\\mu)/\\sigma$; min-max scales to $[0,1]$, "
            "$x' = (x - x_{\\min})/(x_{\\max} - x_{\\min})$. Use standardisation when the model "
            "assumes a Gaussian-like scale. Encoding: one-hot for nominal categories, ordinal for "
            "a genuine ordering."
        ),
        "example": (
            "**Worked problem.** One feature has a missing value and needs z-score scaling. "
            "Train rows: $[4, \\text{NaN}, 6]$, test row: $[8]$.\n\n"
            "**Step 1 — fit on train only.** Impute train mean: $(4+6)/2 = 5$. Train becomes "
            "$[4, 5, 6]$.\n"
            "**Step 2 — train statistics.** $\\mu = (4+5+6)/3 = 5$, "
            "$\\sigma = \\sqrt{((1)^2+(0)^2+(1)^2)/3} = \\sqrt{2/3} \\approx 0.8165$.\n"
            "**Step 3 — scale train.** $z = [(4-5)/0.8165,\\, (5-5)/0.8165,\\, (6-5)/0.8165] \\approx [-1.22, 0, 1.22]$.\n"
            "**Step 4 — test with the SAME numbers.** Impute test with the train mean: $8$ is "
            "complete. Scale: $z = (8-5)/0.8165 \\approx 3.67$.\n"
            "**Step 5 — why it matters.** If you instead scaled test with its own stats, the test "
            "value would be shifted differently and the model would see a distorted distribution at "
            "deployment time. Everything must be re-fitted from the training split."
        ),
        "key_points": [
            "Handle missing values, scale features, encode categories.",
            "Fit imputers/scalers/encoders on the training split only.",
            "Standardisation: $z=(x-\\mu)/\\sigma$; min-max: map to $[0,1]$.",
            "One-hot for nominal categories; ordinal only for real orderings.",
        ],
        "common_mistakes": [
            "Fitting the scaler on all data before splitting — leaks test information.",
            "Imputing the test set with test-derived statistics.",
        ],
        "follow_up_question": "When would you impute with the median instead of the mean, and why does that protect against outliers?",
    },
    "supervised learning": {
        "explanation": (
            "**Supervised learning** learns a mapping from input features $X$ to a target $y$ using "
            "**labelled** examples $(x_i, y_i)$. The goal is not to memorise training pairs but to "
            "*generalise*: perform well on new data the model has never seen. That is why the "
            "protocol is to hold out a test set. Errors split into two kinds. **Bias** is the error "
            "from assuming a model shape that is too simple; **variance** is the extra error from a "
            "model so flexible it chases noise. The bias–variance identity is\n\n"
            "$$\\text{Expected error} = \\text{Bias}^2 + \\text{Variance} + \\text{irreducible noise}$$\n\n"
            "Underfitting is high bias (train error is also high); overfitting is high variance "
            "(train good, test poor). Regularisation, more data and simpler models move you along "
            "the trade-off."
        ),
        "example": (
            "**Worked problem.** You fit a polynomial to 5 points and watch the trade-off as degree $d$ grows.\n\n"
            "**degree 1** (line): train MSE 8.4, test MSE 9.1 → both high = **underfit** (high bias).\n"
            "**degree 3**: train MSE 0.9, test MSE 1.2 → good generalisation balance.\n"
            "**degree 9** (interpolates every point): train MSE 0.0, test MSE 14.7 → train great, "
            "test bad = **overfit** (high variance).\n\n"
            "**Step 1.** Compute both errors, never just the training error.\n"
            "**Step 2.** If train ≈ test but both are high, the model is too simple → add capacity "
            "(features, non-linearity).\n"
            "**Step 3.** If train ≪ test, add regularisation, more data, or reduce capacity.\n"
            "**Step 4.** Repeat until the *gap* plus the *level* of error is acceptable for the task's "
            "cost of mistakes."
        ),
        "key_points": [
            "Requires labelled $(x, y)$ pairs; learns $y \\approx f(x)$.",
            "Generalisation = performance on a held-out test set.",
            "Bias underfits, variance overfits; the identity shows the split.",
            "Diagnose with the train-vs-test error gap.",
        ],
        "common_mistakes": [
            "Tuning hyperparameters on the test set until it leaks.",
            "Judging a model solely by train accuracy.",
        ],
        "follow_up_question": "If adding more training data usually helps, when would it *not* reduce the generalisation error?",
    },
    "model evaluation": {
        "explanation": (
            "**Model evaluation** measures how well a model predicts. For classification the confusion "
            "matrix gives four counts: true positives (TP), false positives (FP), true negatives "
            "(TN), false negatives (FN). From them:\n\n"
            "$$\\text{Precision} = \\frac{\\text{TP}}{\\text{TP}+\\text{FP}}, \\quad "
            "\\text{Recall} = \\frac{\\text{TP}}{\\text{TP}+\\text{FN}}, \\quad "
            "F_1 = 2\\,\\frac{\\text{Precision}\\cdot\\text{Recall}}{\\text{Precision}+\\text{Recall}}$$\n\n"
            "Precision answers 'of those I flagged positive, how many were right?'; recall answers "
            "'of all the real positives, how many did I catch?'. Accuracy is precision's mirror on "
            "imbalanced data: a 95%-negative dataset yields 95% accuracy by predicting nothing as "
            "positive.\n\n"
            "For regression, use MSE/RMSE (same units as $y$), MAE (robust to outliers) and $R^2$. "
            "For ranking, the ROC curve and $\\text{AUC} = $ probability a random positive scores "
            "above a random negative. Always split data first and judge on the untouched test set."
        ),
        "example": (
            "**Worked problem.** A spam filter on 200 emails makes these predictions: real spam "
            "= 100, real ham = 100; predicted 80 spam correctly (TP=80), 20 ham labelled spam "
            "(FP=20), 20 spam missed (FN=20), TN=80.\n\n"
            "**Step 1 — precision.** $80/(80+20) = 80/100 = 0.80$ → 80% of flagged-emails were spam.\n"
            "**Step 2 — recall.** $80/(80+20) = 80/100 = 0.80$ → we caught 80% of real spam.\n"
            "**Step 3 — F1.** $2(0.8)(0.8)/(0.8+0.8) = 1.28/1.6 = 0.80$.\n"
            "**Step 4 — accuracy.** $(80+80)/200 = 0.80$.\n"
            "**Step 5 — interpretation.** Here they agree, but if we had flagged *nothing*, accuracy "
            "would be $100/200 = 0.50$ while precision is undefined and recall $0$ — the metric "
            "choice exposes how broken that model is."
        ),
        "key_points": [
            "Confusion matrix: TP/FP/TN/FN are the raw counts.",
            "Precision $=$ TP/(TP+FP); Recall $=$ TP/(TP+FN); $F_1$ is their harmonic mean.",
            "Accuracy misleads on imbalanced classes.",
            "Always evaluate on a held-out test set.",
        ],
        "common_mistakes": [
            "Using accuracy alone on a 95/5 split.",
            "Comparing AUC reported on training data across models tuned on the test set.",
        ],
        "follow_up_question": "If a high cost is attached to missing spam, which metric — precision or recall — should you optimise and at what threshold?",
    },
    "decision trees": {
        "explanation": (
            "**Decision trees** recursively split the data by asking yes/no questions about a feature, "
            "choosing each split to best separate the classes. The split quality is measured by "
            "**impurity**, most often Gini\n\n"
            "$$\\text{Gini}(C) = 1 - \\sum_{c} p_c^2$$\n\n"
            "where $p_c$ is the fraction of class $c$ in a node. A perfectly pure node has "
            "Gini $= 0$; a balanced mix of two classes has Gini $= 0.5$. The tree picks the feature "
            "and threshold that most reduce the weighted impurity of the children:\n\n"
            "$$\\text{gain} = \\text{Gini}_\\text{parent} - \\left(\\tfrac{n_L}{n}\\,\\text{Gini}_L + \\tfrac{n_R}{n}\\,\\text{Gini}_R\\right)$$\n\n"
            "Splitting stops at a max depth, a minimum samples per leaf, or when a node is pure. "
            "Trees are cheap, interpretable and non-parametric, but a single tree overfits easily "
            "— which is why forests and boosting fix the variance."
        ),
        "example": (
            "**Worked problem.** Two classes in 4 points: $A_1(1,1)$ and $A_2(2,2)$ are class ★, "
            "$B_1(4,4)$ and $B_2(5,5)$ are class ○. Root has $p_★=0.5$, $p_○=0.5$ → "
            "$\\text{Gini}_\\text{root} = 1 - (0.5^2+0.5^2) = 0.5$.\n\n"
            "**Candidate split** $x \\leq 3$ keeps all ★ on the left, all ○ on the right.\n"
            "Left child: all ★ → Gini $= 1 - 1^2 = 0$.\n"
            "Right child: all ○ → Gini $= 0$.\n"
            "Weighted child impurity $= (2/4)(0) + (2/4)(0) = 0$.\n"
            "**Gain** $= 0.5 - 0 = 0.5$ — perfect separation, take the split.\n\n"
            "**Step 1.** Compute parent impurity. **Step 2.** For each candidate split compute "
            "weighted child impurity. **Step 3.** Pick the split with the largest gain. **Step 4.** "
            "Recurse on each child, stopping at depth/stats limits. The $x$-threshold becomes the "
            "tree's first decision; with more data, later splits would handle the diagonal class "
            "patterns."
        ),
        "key_points": [
            "Splits are chosen to reduce impurity (Gini or entropy).",
            "Gini of a mixed node is $1 - \\sum_c p_c^2$; pure = 0.",
            "Depth, min-leaf and purity are natural stopping rules.",
            "Interpretable but high variance — use forests/boosting for stability.",
        ],
        "common_mistakes": [
            "Growing a tree to full depth and reading test metrics off the train score.",
            "Using continuous targets without appropriate split criteria, or ignoring numeric thresholds.",
        ],
        "follow_up_question": "Why is a single deep tree risky in production, and what does limiting `min_samples_leaf` actually change?",
    },
    "knn": {
        "explanation": (
            "**k-Nearest Neighbours** is a non-parametric classifier: it stores the whole training set "
            "and, for a new point, finds its $k$ nearest neighbours by distance (usually Euclidean)\n\n"
            "$$d(x, x') = \\sqrt{\\sum_j (x_j - x'_j)^2}$$\n\n"
            "and predicts by majority vote among them. Because it makes no trained parameters, "
            "inference is a distance computation — fast to train, expensive at prediction time, "
            "and it scales poorly to many features without normalisation. Features on wildly "
            "different scales dominate the distance, so standardising "
            "$z = (x-\\mu)/\\sigma$ matters before fitting. Small $k$ follows local detail (variance, "
            "overfit); large $k$ smooths the boundary (bias, robust). Odd $k$ avoids tie votes."
        ),
        "example": (
            "**Worked problem.** Classify a new point $P(4, 3)$ with $k=3$ from: "
            "$N_1(2,3)$★, $N_2(5,5)$○, $N_3(3,1)$★, $N_4(6,4)$○.\n\n"
            "**Step 1 — distances.**\n"
            "$d(P,N_1)=\\sqrt{(4-2)^2+(3-3)^2} = 2$.\n"
            "$d(P,N_2)=\\sqrt{(4-5)^2+(3-5)^2} = \\sqrt{5} \\approx 2.24$.\n"
            "$d(P,N_3)=\\sqrt{(4-3)^2+(3-1)^2} = \\sqrt{5} \\approx 2.24$.\n"
            "$d(P,N_4)=\\sqrt{(4-6)^2+(3-4)^2} = \\sqrt{5} \\approx 2.24$.\n"
            "**Step 2 — sort.** $N_1$ (2.0), then three neighbours at $\\approx 2.24$.\n"
            "**Step 3 — vote among the 3 nearest.** $N_1$★ and $N_3$★ (tie-break by the next "
            "nearest of $N_2$/`N_4`→) — careful: all three of $N_2, N_3, N_4$ are equidistant, so the "
            "vote depends on the tie rule. If we take $N_3$ over the ○s, ★ wins 2–1.** Let's redo "
            "with a cleaner case: $P(6,3)$, where $d(P,N_4)=1$ is clearly closest, then $d(P,N_1) "
            "\\approx 4.12$, $d(P,N_3) \\approx 3.61$. Nearest three: $N_4$○, $N_3$★, $N_1$★ → ○,★,★ "
            "vote → **★**.\n\n"
            "**Interpretation.** The closest neighbours determine the label; scale the features first "
            "or the distance is meaningless."
        ),
        "key_points": [
            "Stores training data; predicts by majority vote of $k$ nearest neighbours.",
            "Euclidean distance dominates the model, so standardise features.",
            "Small $k$ = high variance; large $k$ = high bias.",
            "No training cost — but prediction is $O(n)$ per query.",
        ],
        "common_mistakes": [
            "Not standardising features, letting a large-scale column drive the votes.",
            "Choosing even $k$ and silently hitting ties.",
        ],
        "follow_up_question": "Why does KNN deteriorate in high dimensions (curse of dimensionality) even though the maths is unchanged?",
    },
    "ensemble methods": {
        "explanation": (
            "**Ensemble methods** combine many weak models into one strong predictor. **Bagging** "
            "(e.g. Random Forest) trains each tree on a bootstrap sample of the data and averages "
            "their votes; averaging uncorrelated errors reduces **variance** "
            "$\\text{Var}(\\bar{X}) = \\sigma^2 / m$. **Boosting** (AdaBoost, gradient boosting, "
            "XGBoost) trains models **sequentially**, each one focusing on the errors of the "
            "previous; adding bias-reducing steps reduces the **bias** step by step.\n\n"
            "Forests are embarrassingly parallel and hard to overfit as you add trees; boosting "
            "needs careful learning rate and depth or it will hammer the training set. Both share "
            "feature-importance heuristics, but they measure *splitting usefulness*, not true causal "
            "importance."
        ),
        "example": (
            "**Worked problem.** Three weak rules predict spam vs ham; combine by majority vote.\n\n"
            "**Rule 1** 'mentions *free* → spam': agrees on 4 of 5 emails, wrong on one ham.\n"
            "**Rule 2** 'long && urgent subject → spam': agrees on 4 of 5, wrong on a different one.\n"
            "**Rule 3** 'has link count > 2 → spam': agrees on 4 of 5, wrong on yet another.\n\n"
            "**Step 1.** For email $e_1$, votes: spam, spam, ham → majority **spam**.\n"
            "**Step 2.** For email $e_4$ (no individual rule fires, active learning: two say ham) → "
            "ham.\n"
            "**Step 3.** The ensemble errs only where at least two rules agree wrongly. If each rule "
            "is right 80% of the time and their errors are mostly independent, the majority of 3 is "
            "right $0.8^3 + 3(0.8^2)(0.2)=0.512+0.384=0.896$ — about 90%.\n"
            "**Step 4.** Random Forest does this with ~500 trees; boosting instead reweights the "
            "examples each weak learner gets wrong, so later trees carve up the leftovers."
        ),
        "key_points": [
            "Bagging bootsamples + averages → cuts variance.",
            "Boosting is sequential → focuses on earlier mistakes, cuts bias.",
            "Random Forest is parallel and robust; boosting needs depth/LR tuning.",
            "Feature importances rank split usefulness, not causation.",
        ],
        "common_mistakes": [
            "Judging a boosting model by train accuracy (it can hit ~100% and still generalise badly).",
            "Reading feature importance tables as a causal ranking of what matters.",
        ],
        "follow_up_question": "Why can a Random Forest with many trees be safe to grow, while gradient boosting with too many rounds overfits?",
    },
    "feature engineering": {
        "explanation": (
            "**Feature engineering** constructs the inputs a model learns from. The goal is to fold "
            "domain structure into columns the model can exploit simply. Common moves: **transforms** "
            "(log or square to linearise effects), **interaction terms** "
            "$x_{12} = x_1 \\cdot x_2$ when the effect of one feature depends on another, "
            "**polynomials** $x^2, x^3$ for curvature, and **derived signals** (hour of day, day of "
            "week, ratios, differences).\n\n"
            "Correctness matters more than cleverness: if any engineered feature is computed with "
            "information that would not be available at prediction time (e.g. fitted on the whole "
            "dataset), you have leaked the target and inflated your scores."
        ),
        "example": (
            "**Worked problem.** Predict price per sq ft from area $x$ and bedrooms; the marginal "
            "value of a bedroom differs with area (bigger house → each bedroom costs more), so add "
            "the product.\n\n"
            "**Step 1 — base features.** $x_1 = \\text{area}$ (sq ft), $x_2 = \\text{bedrooms}$.\n"
            "**Step 2 — interaction.** $x_3 = x_1 \\cdot x_2 = \\text{area} \\times \\text{bedrooms}$.\n"
            "**Step 3 — inspect.** A 1,000 sq ft, 3-bed home gives $x_3 = 3000$; a 1,000 sq ft "
            "1-bed gives $x_3 = 1000$ — the model can now learn 'each extra bedroom is worth more "
            "when the house is larger' with a single linear term.\n"
            "**Step 4 — scale first.** With area in the thousands, standardise "
            "($z = (x-\\mu)/\\sigma$) before fitting or the interaction dominates the gradient.\n"
            "**Step 5 — verify.** Check the out-of-sample MAE improves versus the model without the "
            "interaction; if not, drop it."
        ),
        "key_points": [
            "Transform, create interactions/polynomials, derive domain signals.",
            "Interactions let one feature moderate another's effect.",
            "Standardise before fitting so scales don't dominate.",
            "Never engineer with data you wouldn't have at prediction time.",
        ],
        "common_mistakes": [
            "Adding an interaction without scaling, letting it dominate the loss.",
            "Fitting target statistics (e.g. mean target by group) into features = leakage.",
        ],
        "follow_up_question": "Why is a target-encoded mean-of-y-by-category feature leakage when fitted on the full dataset?",
    },
    "model deployment": {
        "explanation": (
            "**Model deployment** is the engineering of a trained model into production. The model "
            "itself is a service behind an API; inputs are transformed by preprocessing that must "
            "match training exactly (same scaler object, same feature list, same vocabulary), then "
            "the model returns predictions. The recurring failure is **train/serve skew** — the "
            "distribution of live inputs drifts away from what the model saw. The two tools are "
            "*monitoring* (track prediction distribution, data drift, and the actual outcome when it "
            "arrives) and *controlled release* (shadow deploy the new model beside the old one and "
            "compare predictions before switching traffic).\n\n"
            "Latency and throughput are as real as accuracy: models get batch-scored or moved behind "
            "a feature store, and only shadow-deployed when confidence is high."
        ),
        "example": (
            "**Worked problem.** You trained a demand-forecast model offline with 95% R²; in "
            "production, forecast error triples. Walk the deployment pipeline.\n\n"
            "**Step 1 — check preprocessing.** Was the scaler fitted on the full dataset rather than "
            "the training fold? If so, the live pipeline is re-fitting on incoming data → verify the "
            "frozen scaler object is being reused.\n"
            "**Step 2 — check features.** Does the live request supply the same columns, dtypes and "
            "encodings? Missing categories that were never in the vocabulary silently become NaN.\n"
            "**Step 3 — check the data drift.** Compute the live feature mean/std versus training; "
            "if the mean shifted, the trained boundary is now in the wrong place.\n"
            "**Step 4 — shadow deploy.** Run the new candidate beside the champion for a week, log "
            "both predictions, compare on realised outcomes, then switch traffic.\n"
            "**Step 5 — monitor.** Set alerts on prediction drift and label-lag so the next quiet "
            "failure is an alert, not a surprise."
        ),
        "key_points": [
            "Ship frozen preprocessing + the same feature contract as training.",
            "Train/serve skew is the top silent failure; monitor for it.",
            "Shadow deploy new candidates before switching traffic.",
            "Latency, drift and label lag are production metrics, not just accuracy.",
        ],
        "common_mistakes": [
            "Retraining scalers/encoders in the serving path.",
            "Releasing on offline R² without a shadow comparison.",
        ],
        "follow_up_question": "Why does a model that scored well on the test set still deserve shadow deployment before full release?",
    },
"python for ml": {
        "explanation": (
            "**Python for ML** is the toolchain that turns data into models: NumPy for arrays, "
            "Pandas for tables, scikit-learn for the model zoo, and Matplotlib for inspection. The "
            "recurring pattern is a **pipeline** — load data, clean and split, fit a model, "
            "evaluate, iterate. Because `scikit-learn` models expose a uniform "
            "`fit(X, y)` / `predict(X)` / `score(X, y)` interface, swapping one algorithm for "
            "another is a one-line change, which makes experimentation cheap.\n\n"
            "The other essential habit is reproducibility: pin library versions, set a fixed "
            "`random_state` for anything stochastic, and keep the train/test split fixed so two "
            "prototypes are comparable."
        ),
        "example": (
            "**Worked problem.** Stand up a minimal, honest ML loop on three steps of data.\n\n"
            "```python\n"
            "import numpy as np\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.metrics import mean_absolute_error\n"
            "\n"
            "X = np.array([[2.], [3.], [5.], [7.], [11.]])\n"
            "y = np.array([4., 6., 10., 14., 22.])\n"
            "\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "    X, y, test_size=0.4, random_state=7)\n"
            "model = LinearRegression()\n"
            "model.fit(X_tr, y_tr)\n"
            "pred = model.predict(X_te)\n"
            "print(mean_absolute_error(y_te, pred))\n"
            "```\n"
            "**Step 1** split before scaling/fitting. **Step 2** fit only on the training fold. "
            "**Step 3** score on the test fold with an error metric in the target's units. Because "
            "$y = 2x$ exactly, near-perfect MAE is expected — real data never is, which is exactly "
            "why the train/test ritual matters."
        ),
        "key_points": [
            "NumPy (arrays) + Pandas (tables) + scikit-learn (models).",
            "Uniform `fit`/`predict`/`score` interface across algorithms.",
            "Split, fit, evaluate — treat test data as invisible until scoring.",
            "Pin versions and `random_state` for reproducible experiments.",
        ],
        "common_mistakes": [
            "Fitting the scaler on the whole dataset before the train/test split.",
            "Forgetting `random_state`, so 'improvements' are just seed luck.",
        ],
        "follow_up_question": "Why does setting a fixed `random_state` matter when comparing two models, and what does `test_size=0.4` imply for a 5-sample dataset?",
    },
}
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
