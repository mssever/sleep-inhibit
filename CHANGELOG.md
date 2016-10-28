## [Unreleased]
### Fixed
- Docstring for `sleepinhibit.config._settingsObject.init` was outdated and hadn't
been updated.

### Cleaned up
- API improvements for `sleepinhibit.collection.Collection`
- Adjusted `sleepinhibit.config._SettingsObject` to use the revised API instead of
  calling `__setattr__` directly.

## [1.0.0]
### Added
- System to build .deb files

### Fixed
- Inhibit/Enable toggle now works correctly (issue #7)
- Starting without an X session now results in a more understandable error
  message (issue #11)
- Renamed the two different `settings` modules to tame confusion. Now, the
  user-facing preferences dialog is in `sleepinhibit.gui.prefs` and the
  non-user-facing configuration class is in `sleepinhibit.config`. Related
  classes and other names have also been updated. (Issue #12)
- Numerous minor fixes

## [1.0.0~beta] - 2016-05-11
### Initial Release
