from quality import compute_quality_for_corpus

from simple_filters import RandomFilter as Filter

TRAINING_DIRECTORY = "./assets/1/"
TESTING_DIRECTORY = "./assets/2/"

if __name__ == "__main__":
    filter = Filter()
    filter.train(TRAINING_DIRECTORY)
    filter.test(TESTING_DIRECTORY)
    quality = compute_quality_for_corpus(TESTING_DIRECTORY)
    print(f"Filter has quality: {quality}")
