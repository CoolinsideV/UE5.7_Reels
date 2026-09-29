# @Description: dump bp pins v2
import unreal
TARGET = ('DrawTexture','DrawMaterialToRenderTarget','BeginDrawCanvasToRenderTarget',
          'EndDrawCanvasToRenderTarget','ClearRenderTarget2D','CreateDynamicMaterialInstance',
          'SetVectorParameterValue','SetWorldTransform')
bp = unreal.load_asset('/Game/DeformableSnow/BluePrint/BP_Board')
lib = unreal.BlueprintEditorLibrary
for gname in ('EventGraph','UserConstructionScript','WorldPositionToUV','UpdatePosition','CopySnow'):
    try:
        g = lib.find_graph(bp, gname)
    except Exception as e:
        print('GRAPH %s load fail %s' % (gname, e)); continue
    if not g:
        print('GRAPH %s NOT FOUND' % gname); continue
    try:
        nodes = list(g.get_editor_property('nodes'))
    except Exception as e:
        print('GRAPH %s nodes fail: %s' % (gname, e))
        print('  graph attrs:', [a for a in dir(g) if not a.startswith('_')][:40])
        continue
    for n in nodes:
        cn = n.get_class().get_name()
        if cn != 'K2Node_CallFunction':
            continue
        fn = ''
        try:
            fn = str(n.get_editor_property('function_reference').get_editor_property('member_name'))
        except Exception:
            pass
        if fn not in TARGET:
            continue
        print('NODE %-36s graph=%s' % (fn, gname))
        try:
            pins = list(n.get_editor_property('pins'))
        except Exception as e:
            print('    pins fail', e); continue
        for p in pins:
            try: nm = str(p.get_editor_property('pin_name'))
            except Exception: nm = '?'
            try: dv = str(p.get_editor_property('default_value'))
            except Exception: dv = ''
            try:
                o = p.get_editor_property('default_object')
                do = o.get_path_name() if o else ''
            except Exception: do = ''
            try: nlk = len(list(p.get_editor_property('linked_to')))
            except Exception: nlk = -1
            if dv or do or nlk == 0:
                print('    %-24s def=%-18s obj=%-50s links=%s' % (nm, dv, do, nlk))
