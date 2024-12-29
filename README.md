# Spam filter

This is an implementation of a spam filter using Naive Bayes filtering in
Python for course Solving Problems and Other Games which is taught at CTU FEE.
The instructions for the task are available on the [course's
website](https://cw.fel.cvut.cz/b241/courses/b4b33rph/cviceni/spam/start).

## Dependencies

- BeautifulSoup4

## Running

The code can be cloned as follows:

```
git clone https://github.com/SimonBrandner/rph-spam-filter
```

To test the spam filter on a dataset `path/to/dataset_name`, you can move the
dataset as follows:

```
mkdir -p rph-spam-filter/src/assets
mv path/to/dataset_name rph-spam-filter/src/assets/dataset_name
```

You can run the spam filter using the following:

```
rph-spam-filter/src
python test.py
```
