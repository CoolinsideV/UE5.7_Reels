/** @UnrealClaude Script
 * @Description: Dump BP_Board pin defaults incl. object refs */
import unreal

bp = unreal.load_asset('/Game/DeformableSnow/BluePrint/BP_Board')
lib = unreal.BlueprintEditorLibrary
graphs = lib.get_blueprint_all_graphs(bp)
for g in graphs:
    gname = g.get_name()
    try:
        nodes = g.get_editor_property('nodes')
    except Exception as e:
        print('GRAPH %s : cannot read nodes (%s)' % (gname, e)); continue
    print('==== GRAPH %s (%d nodes)' % (gname, len(nodes)))
    for n in nodes:
        cn = n.get_class().get_name()
        if cn != 'K2Node_CallFunction':
            continue
        fn = ''
        try:
            fn = n.get_editor_property('function_reference').get_editor_property('member_name')
        except Exception:
            pass
        if fn not in ('DrawTexture','DrawMaterialToRenderTarget','BeginDrawCanvasToRenderTarget',
                      'EndDrawCanvasToRenderTarget','ClearRenderTarget2D','CreateDynamicMaterialInstance',
                      'SetVectorParameterValue','K2_DrawTexture','SetWorldTransform'):
            continue
        print('  NODE %s  (%s)' % (fn, cn))
        for p in n.get_editor_property('pins'):
            try:
                nm = p.get_editor_property('pin_name')
            except Exception:
                continue
            dv = ''
            do = ''
            try: dv = str(p.get_editor_property('default_value'))
            except Exception: pass
            try:
                o = p.get_editor_property('default_object')
                do = o.get_path_name() if o else 'None'
            except Exception: do = 'n/a'
            if dv or do not in ('n/a','None'):
                print('      %-26s value=%-14s object=%s' % (nm, dv, do))
