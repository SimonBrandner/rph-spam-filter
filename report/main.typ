#import "template.typ": *
#import "@preview/metalogo:1.1.0": LaTeX

#show: project.with(
  title: "Spam Filter",
  authors: (
    (
      name: "Šimon Brandner",
      email: "brandsi1@cvut.cz",
      affiliation: "Faculty of Electrical Engineering,\n Czech Technical University",
    ),
    (
      name: "Jiří Král",
      email: "kralji17@cvut.cz",
      affiliation: "Faculty of Electrical Engineering,\n Czech Technical University",
    ),
  ),
  abstract: [We were tasked with implementing a spam filter in Python in whatever way. We chose the Beautiful Soup library for parsing individual e-mails and Naive Bayes filtering for classification. We achieved fast and accurate results (75% - 95% depending on the dataset). In this report, we also mention other tools used during development as well as the organization of teamwork.],
  date: "January 5, 2025",
)

= Introduction

This semestral work aimed to implement a spam filter in Python -- a binary classifier that categorizes emails as either _spam_ or _ham_ (not spam). Individual emails are represented as text files formatted according to #link("https://www.rfc-editor.org/rfc/rfc5322.html")[RFC 5322]. Given a _dataset_ (a directory with e-mails), the spam filter creates a special file `!prediction.txt` (according to the #link("https://cw.fel.cvut.cz/wiki/courses/b4b33rph/cviceni/spam/krok6#specifikace")[specification]) which contains the classification of each e-mail in the form of key-value pairs in the format `<email-file-name> <OK | SPAM>` separated by newlines.

However, before the spam filter can classify e-mails, it must first be trained on a dataset where the correct classification of all e-mails is known beforehand and written in file `!truth.txt` (which has the same format as `!prediction.txt`).

The spam filter adheres to the specification which can be found on the course's
#link("https://cw.fel.cvut.cz/wiki/courses/b4b33rph/cviceni/spam/krok6#specifikace")[webpage] and its #link("https://github.com/SimonBrandner/rph-spam-filter")[source code] has been made public on GitHub.

= Implementation

We focus on parsing and filtering in this section as that is the core of the spam filter and the other work that was done is not particularly interesting.

== Parsing

Given an email formatted according to the RFC 5322 standard, we split it into a head section containing all the metadata and a body section containing the content of the email itself.

From the head, we extract the `From` entry, which contains the address of the sender, and the `Subject` entry of the email containing the subject. The `From` entry is mandatory and should be present in every email formatted according to the standard. The `Subject` entry is not mandatory but is present in almost every email. If the `Subject` entry is not present, it is treated as if it was an empty string.

If HTML markup is present in the body of the email, it is removed using Python's #link("https://pypi.org/project/beautifulsoup4/")[Beautiful Soup] @beautiful-soup-docs library like so:

```python
from bs4 import BeautifulSoup
# ...
soup = BeautifulSoup(text_with_markup, 'html.parser')
text_without_markup = soup.get_text()
```

`From`, `Subject` and the body of the e-mail is then split into words at whitespace characters with each word being converted to lowercase. The set of all these words is called a _bag of words_ (see @naive-bayes) used as input for the Naive Bayes filter described in the next section.

== Naive Bayes <naive-bayes>

We decided to opt for Naive Bayes @statquest-naive-bayes filtering as it seemed relatively straightforward and quick to implement, so it would offer a quick win if it worked. Another benefit of this approach is its speed. As the name implies, this approach is considered naive since it uses what we call a _bag of words_ -- it does not consider the word order at all @statquest-naive-bayes. That said, it still produces relatively accurate results (see @results).

=== Notation

As e-mails often include the same word multiple times, we will use the concept of a _multiset_ which, unlike a regular _set_, allows for multiple instances of the same element. We define $abs(A)$ as the size of the multiset $A$, $A union.plus B$ as the union of multisets $A$ and $B$ and $"freq"(m, M)$ as the number of occurrences of element $m$ in the multiset $M$.

Let $E$ be the multiset of all e-mails, $S subset.eq E$ be the multiset of all spams and $H subset.eq E$ be the multiset of all hams. We view any e-email $e in E$ as a multiset of words $w in e$. Let $W_"spam" = union.plus.big_(s in S) s$ be the multiset of all words in spams and $W_"ham" in union.plus.big_(h in H) h$ be the multiset of all words in hams. Let $W = W_"spam" union.plus W_"ham"$ be the multiset of all words.

=== Training

During training, we compute the likelihood that any e-mail is spam

$ accent(P, ~)_"spam" = frac(abs(S), abs(E)), $

and the likelihood that any e-mail is ham

$ accent(P, ~)_"ham" = frac(abs(H), abs(E)). $

Later during training, for each word $w in W$ we compute the likelihood that it appears in spam

$
  accent(P, hat)_"spam" (w) = frac("freq"(w, W_"spam")+1, |W_"spam"|),
$ <probability-of-spam-of-word>

and the likelihood that the word $w in W$ appears in ham

$
  accent(P, hat)_"ham" (w) = frac("freq"(w, W_"ham")+1, |W_"ham"|).
$ <probability-of-ham-of-word>

=== Filtering

During filtering, for any given e-mail $e in E$, we compute the likelihood that it is spam

$
  P_"spam" (e) = accent(P, ~)_"spam" product_(w in e) accent(P, hat)_"spam" (w),
$

and the likelihood that the e-mail is ham

$ P_"ham" (e) = accent(P, ~)_"ham" product_(w in e) accent(P, hat)_"ham" (w). $

If $P_"spam" < P_"ham"$, we say a given e-mail is ham, otherwise, it is spam.

We can now also see the $+1$ in @probability-of-spam-of-word and @probability-of-ham-of-word is very important. Without it, if a $w in.not W_"spam"$ or $w in.not W_"ham"$ but $w in e$, $P_"spam" (e)$ or $P_"ham" (e)$ would equal $0$ respectively @statquest-naive-bayes.


= Methodology

We were provided with two data sets, in this section we describe our methodology for testing the spam filter on these two datasets.

== Quality of a spam filter

We base our measurement of the quality of the filter on the _binary confusion matrix_ (see @binary-confusion-matrix) which is the result of comparing the predicted classification (the one generated by the classifier) with the actual classification. We consider the case where e-mail is spam to be positive.

#figure(
  table(
    stroke: none,
    align: center + horizon,
    table.hline(y: 0, start: 2),
    table.hline(y: 1, start: 2),
    table.hline(y: 2, start: 0),
    table.hline(y: 3, start: 1),
    table.hline(y: 4, start: 0),
    table.vline(x: 0, start: 2),
    table.vline(x: 1, start: 2),
    table.vline(x: 2, start: 0),
    table.vline(x: 3, start: 1),
    table.vline(x: 4, start: 0),
    columns: (auto, auto, auto, auto),
    [], [], table.cell(colspan: 2, [*Predicted class*]),
    [], [], [*Positive*], [*Negative*],
    table.cell(rowspan: 2, rotate(-90deg, reflow: true)[*Actual class*]),
    rotate(-90deg, reflow: true)[*Positive*],
    [True Positive #linebreak() (*TP*)], [False Negative #linebreak() (*FN*)],
    rotate(-90deg, reflow: true)[*Negative*],
    [False Positive #linebreak() (*PN*)], [True negative #linebreak() (*TN*)],
  ),
  caption: [Binary confusion matrix],
) <binary-confusion-matrix>

After the spam filter classifies e-mails in a given dataset, we compute how many e-mails are in each category (TP, TN, FP, FN). Based on this we compute the quality

$ q = frac("TP" + "TN", "TP" + "TN" + 10 "FP" + "FN") $ <quality>

of the filter for the dataset. In @quality we multiply $"FP"$ $10$ times since we consider the case where a user does not receive a ham to be worse than if they received spam.

== Data splitting <data-splitting>

A testing script (located in `src/test.py`) was created for running the spam filter on the provided datasets. First, it randomly splits the dataset into two parts --- the _training set_ and the _testing set_ (with a ratio of 4:1). Later, it runs the ```py BaseFilter.train()``` method on the training set and ```py BaseFilter.test()``` on the testing set. This process can be run multiple times for each dataset to make sure the randomness did not introduce any bias.

= Results <results>

Our spam filter implementation gives quite good results and achieves high-quality $q$. Specifically, it gets $q_1 = 93%$ for the first provided dataset and $q_2 = 89%$ for the second provided dataset with $250$ runs of the testing code (as described in @data-splitting).

We were surprised by how well Naive Bayes handles non-words in email and especially how well it performs even when it treats words that have punctuation before or after them as separate words. By non-words in this case, we mean any content other than normal words and HTML markup (which we have stripped out) that we can find in an email, such as URLs, random data etc.

Removing all punctuation from the text of an email, and limiting the length of what we still consider a word to 25 characters, made the dictionary of words captured by the algorithm smaller and cleaner. However, it did not improve the results noticeably.

While punctuation characters such as `!` or `?` play an important role in the overall tone and meaning of an email, other characters such as `(` and `,` may play a much smaller role and probably don't hold any information that would give a word much of an extra meaningful value for it to make sense to be treated differently.

We were also surprised by how effective the bag of words approach can be even though it glosses over a lot of nuance.

= Teamwork

This semestral work was a team project, in this section, we detail how the work was organized and performed, what tools were used for communication and collaboration etc.

== Division of labour

In table @division-of-labor-table we show what tasks were done by each team member.

#figure(
  table(
    columns: (auto, auto),
    table.header([*Task*], [*Author*]),
    [Email parsing], [Král],
    [Text normalization], [Král],
    [Naive Bayes filtering], [Brandner],
    [Report], [Both],
  ),
  caption: [Division of labour],
) <division-of-labor-table>

== Tools

We opted for Git as our version control software since it is the de facto standard. We used GitHub as the cloud service on which to host our Git repository. GitHub was also a great choice given its code collaboration features such as pull requests which enabled us to effectively communicate our ideas about code.

For real-time communication, we tried several services (e.g. Matrix, WhatsApp) but in the end stuck to WhatsApp as it turned out to be the most stable. However, we were not happy with the features WhatsApp offered. While its text formatting features have improved in recent years, they are nowhere close to what some other services offer (code blocks etc.). The closed-source nature of WhatsApp is also not entirely to our liking, so we'd certainly like to give protocols such as Matrix a second chance in the future.

For writing this report, we decided to try #link("https://typst.app/")[Typst], a modern alternative to #LaTeX written in #link("https://www.rust-lang.org/")[Rust], which offers simpler syntax, faster compile times and builtin online editor. While it does not offer complete feature parity with #LaTeX, we have enjoyed working with it, as its simpler syntax makes writing text faster and it does not produce hard-to-parse error messages. We would say it was more than adequate for our needs.

= Conclusion

Our task was to implement a spam filter in Python using whatever algorithm. We opted for parsing the emails' content and Naive Bayes filtering. Using these methods we were able to implement a filter with high accuracy. The project allowed us to learn new things and gain experience in the fields of statistics, analysis, Python, code collaboration, versioning, testing, and teamwork management.
