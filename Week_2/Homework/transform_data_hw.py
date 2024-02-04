if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Remove rows with 0 passenger counts and trip distances.
    Convert column names to smallcase
    Create new column to host lpep_pickup_datetime date objects
    """
    # Passenger Counts > 0
    data = data[data['passenger_count'] > 0]

    # Trip distance > 0
    data = data[data['trip_distance'] > 0]

    # Change columns names to snake_case
    columns = {
        'VendorID': 'vendor_id',
        'RatecodeID': 'rate_code_id', 
        'PULocationID': 'pu_location_id', 
        'DOLocationID': 'do_location_id',
    }

    data = data.rename(columns=columns)

    # Unique values of VendorID
    print(f"Existing values of VendorID in the dataset: {data.vendor_id.unique()}")

    return data 


@test
def test_output(output, *args) -> None:
    """
    Assertion block for vendor id.
    """
    assert 'vendor_id' in output.columns, 'vendor_id missing in column names.'


@test
def test_output(output, *args) -> None:
    """
    Assertion block for passenger count.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'Output has 0 passenger count rows.'


@test
def test_output(output, *args) -> None:
    """
    Assertion block for trip distance.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'Output has 0 trip distance rows.'