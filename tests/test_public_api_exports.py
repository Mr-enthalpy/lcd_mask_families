import lcd_mask_families as api


def test_public_api_exports_v0_1_contract_symbols_only():
    expected = {
        "__version__",
        "CONTRACT_VERSION",
        "MaskFamilySpec",
        "MaskInstanceSpec",
        "MaskSequenceSpec",
        "GridSpec",
        "ProjectionSpec",
        "MaskIdentity",
        "RenderedMask",
        "render_continuous_mask",
        "project_display_mask",
        "render_display_mask",
        "render_mask_instance",
        "render_mask_sequence",
        "canonicalize_spec",
        "hash_mask_instance",
        "hash_mask_sequence",
        "load_mask_instance_spec",
        "load_mask_sequence_spec",
        "dump_mask_instance_spec",
        "dump_mask_sequence_spec",
        "list_families",
        "get_family_metadata",
    }

    assert set(api.__all__) == expected
    for name in expected:
        assert hasattr(api, name)


def test_contract_version_is_v0_1():
    assert api.__version__ == "0.1.0"
    assert api.CONTRACT_VERSION == "lcd_mask_families.v0.1"
