# @UnrealClaude Script
# @Description: Dump BP_Board pin defaults incl object refs
import unreal

TARGET_FN = ('DrawTexture','DrawMaterialToRenderTarget','BeginDrawCanvasToRenderTarget',
             'EndDrawCanvasToRenderTarget','ClearRenderTarget2D','CreateDynamicMaterialInstance',
             'SetVectorParameterValue','SetWorldTransform')

bp = unreal.load_asset('/Game/DeformableSnow/BluePrint/BP_Board')
graphs = []
for prop in ('ubergraph_pages','function_graphs'):
    try:
        graphs.extend(list(bp.get_editor_property(prop)))
    except Exception as e:
        print('prop %s fail: %s' % (prop, e))

print('TOTAL GRAPHS', len(graphs))
for g in graphs:
    gname = g.get_name()
    try:
        nodes = list(g.get_editor_property('nodes'))
    except Exception as e:
        print('GRAPH %s: %s' % (gname, e)); continue
    for n in nodes:
        cn = n.get_class().get_name()
        if cn != 'K2Node_CallFunction':
            continue
        fn = ''
        try:
            fr = n.get_editor_property('function_reference')
            fn = str(fr.get_editor_property('member_name'))
        except Exception:
            pass
        if fn not in TARGET_FN:
            continue
        print('NODE %-38s graph=%s' % (fn, gname))
        try:
            pins = list(n.get_editor_property('pins'))
        except Exception as e:
            print('   pins fail', e); continue
        for p in pins:
            try:
                nm = str(p.get_editor_property('pin_name'))
            except Exception:
                continue
            dv = ''
            do = ''
            try: dv = str(p.get_editor_property('default_value'))
            except Exception: pass
            try:
                o = p.get_editor_property('default_object')
                do = o.get_path_name() if o else ''
            except Exception: pass
            try:
                lk = p.get_editor_property('linked_to')
                nlk = len(lk) if lk else 0
            except Exception:
                nlk = -1
            if dv or do or nlk == 0:
                print('   %-26s def=%-16s obj=%-52s links=%s' % (nm, dv, do, nlk))
