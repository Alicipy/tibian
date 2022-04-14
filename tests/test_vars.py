def test_public_imports():

    import tibian.vars as tv

    assert tv.get_today()
    assert tv.get_std_config_filepath()
