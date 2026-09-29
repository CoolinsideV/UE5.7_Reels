# @Description: probe play api
import unreal
for cls in ('LevelEditorSubsystem','UnrealEditorSubsystem','EditorLevelLibrary'):
    try:
        c = getattr(unreal, cls)
    except Exception as e:
        print(cls, 'MISSING'); continue
    print(cls, ':', [a for a in dir(c) if not a.startswith('_') and ('play' in a.lower() or 'pie' in a.lower() or 'game' in a.lower() or 'world' in a.lower())])
