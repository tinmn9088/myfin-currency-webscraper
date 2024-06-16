import myfin


def test_extract_area():

    # arrange
    link = 'https://myfin.by/currency/minsk'
    expected = 'minsk'

    # act
    actual = myfin.MyfinService.extract_area(link)

    # assert
    assert expected == actual
