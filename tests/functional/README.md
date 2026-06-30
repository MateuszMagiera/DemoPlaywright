# Functional Tests — DemoQA

End-to-end Playwright tests targeting [DemoQA](https://demoqa.com).

## Running

```bash
# All functional tests (from project root)
pytest tests/functional/ -v

# Smoke tests only (fast, ~1min)
pytest tests/functional/ -m smoke -v

# Skip slow tests (progress bar waits)
pytest tests/functional/ -m "not slow" -v

# Single file
pytest tests/functional/test_forms.py -v
```

## Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `test_forms.py` | 16 | TextBox, CheckBox, RadioButton |
| `test_widgets.py` | 15 | Slider, ProgressBar, Tabs |
| `test_alerts.py` | 8 | Alerts, Confirm, Prompt, Browser Windows |

## Adding a New Test

1. Create or find the page object in `src/pages/`
2. Add fixture in `conftest.py`
3. Write test with `@pytest.mark.smoke` (happy path) or `@pytest.mark.regression`

```python
@pytest.mark.smoke
def test_example(my_page: MyPage) -> None:
    my_page.do_action()
    assert my_page.get_result() == "expected"
```

## Markers

- `@pytest.mark.smoke` — happy path, run on every push
- `@pytest.mark.regression` — full suite
- `@pytest.mark.slow` — tests that take > 10s (excluded from fast runs)
