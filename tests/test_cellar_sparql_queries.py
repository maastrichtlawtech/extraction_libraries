from cellar_extractor.cellar_sparql_queries import CellarSparqlQuery


import pytest

# List of CELEX numbers
celex = ["61963CO0111"]


@pytest.mark.parametrize("celex", celex)
def test_get_endorsement(celex):
    result = CellarSparqlQuery().get_endorsements(celex)
    ground_truth = (
        "\n\nON THOSE GROUNDS,  \n"
        "UPON HEARING THE REPORT OF THE JUDGE-RAPPORTEUR;  \n"
        "UPON HEARING THE PARTIES TO THE MAIN ACTION AND THE INTERVENER;  \n"
        "UPON HEARING THE OPINION OF THE ADVOCATE-GENERAL;"
    )
    # Strip trailing whitespace
    result = result.rstrip()
    ground_truth = ground_truth.rstrip()
    # Strip newlines
    result = result.replace("\n", "")
    ground_truth = ground_truth.replace("\n", "")
    assert result == ground_truth


# This test is currently failing and needs to be 
# sorted out in the future.
celex = ["61986CJ0062"]
@pytest.mark.parametrize("celex", celex)
def test_get_grounds(celex):
    result = CellarSparqlQuery().get_grounds(celex)
    # Read ground truth from file 61986CJ0062.ENG.txt
    with open("61986CJ0062.ENG.txt", "r") as f:
        ground_truth = f.read()
    # Remove <p> tags from ground truth
    ground_truth = str(ground_truth).replace("<p>", "").replace("</p>", "")
    # Strip leading and trailing whitespace
    result = result.strip()
    ground_truth = ground_truth.strip()
    # Strip newlines
    result = result.replace("\n", "")
    ground_truth = ground_truth.replace("\n", "")
    assert result == ground_truth

# Run the tests
if __name__ == "__main__":
    pytest.main(["-vv"])
