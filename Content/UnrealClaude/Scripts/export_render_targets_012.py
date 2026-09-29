# @Description: export render targets
import unreal
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
w = ues.get_editor_world()
print('editor world:', w)
krl = unreal.KismetRenderingLibrary
out = 'E:/UE5works/Practice/Showreels/Saved/claude/'
for name in ('RT_Snow', 'RT_SnowSave'):
    rt = unreal.load_asset('/Game/DeformableSnow/Texture/' + name)
    for fn in ('export_render_target', 'export_texture2d'):
        try:
            getattr(krl, fn)(w, rt, out, name + '.png')
            print('exported', name, 'via', fn); break
        except Exception as e:
            print('  %s.%s failed: %s' % (name, fn, e))
