# QA Workflows

## Table of Contents
- [Smoke Test (Login Example)](#smoke-test-login-example)
- [Locator Strategy](#locator-strategy)
- [Common Patterns](#common-patterns)

## Smoke Test (Login Example)

```
1) qa_refresh_and_list_windows()
2) select_application_window(id, name)
3) capture_window_screenshot()
4) get_app_window_controls_info(field_list=["label","control_text","control_type","automation_id","control_rect"])
5) set_edit_text(id, name, "username_value")
6) set_edit_text(id, name, "password_value")
7) click_input(id, name)   # login button
8) qa_wait_for_text_contains(id, name, "Welcome", timeout_s=10)
9) capture_window_screenshot()
```

## Locator Strategy

1. Prefer control IDs from `get_app_window_controls_info`
2. Use `automation_id` as a human-readable secondary anchor when available
3. Re-collect controls after navigation or dialog open (control tree changes)
4. Use coordinate actions only as last resort, with a comment explaining why

## Common Patterns

**Form fill + submit**: collect controls -> set_edit_text for each field -> click_input on submit -> assert result text

**Navigation**: click menu/tab -> re-collect controls -> verify new view via screenshot + texts()

**Dialog handling**: after triggering dialog, re-collect controls (new control tree) -> interact -> close dialog -> re-collect parent window controls

**Data grid verification**: collect controls -> find grid cells by control_text -> compare against expected values
