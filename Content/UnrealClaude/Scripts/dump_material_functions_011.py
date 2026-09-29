# @Description: dump material functions
import unreal
mel = unreal.MaterialEditingLibrary

def walk(m, e, d, seen):
    if e is None: return
    k = e.get_path_name()
    if k in seen or d > 12: return
    seen.add(k)
    cls = e.get_class().get_name()
    extra = ''
    try:
        if 'CollectionParameter' in cls:
            extra = 'PARAM=%s  coll=%s' % (e.get_editor_property('parameter_name'), e.get_editor_property('collection').get_name() if e.get_editor_property('collection') else None)
        elif 'TextureSample' in cls:
            extra = 'tex=%s' % e.get_editor_property('texture').get_name()
        elif 'VectorParameter' in cls:
            extra = 'PARAM=%s' % e.get_editor_property('parameter_name')
        elif 'ScalarParameter' in cls:
            extra = 'PARAM=%s' % e.get_editor_property('parameter_name')
        elif cls == 'MaterialExpressionConstant':
            extra = 'r=%s' % e.get_editor_property('r')
        elif cls == 'MaterialExpressionConstant2Vector':
            extra = 'rg=(%s,%s)' % (e.get_editor_property('r'), e.get_editor_property('g'))
        elif cls == 'MaterialExpressionFunctionInput':
            extra = 'in=%s' % e.get_editor_property('input_name')
        elif 'ComponentMask' in cls:
            extra = 'rgba=(%s,%s,%s,%s)' % (e.get_editor_property('r'), e.get_editor_property('g'), e.get_editor_property('b'), e.get_editor_property('a'))
    except Exception as ex:
        extra = '(<%s>)' % ex
    print('  ' * d + cls + '   ' + extra)
    try:
        ins = list(mel.get_inputs_for_material_expression(m, e))
    except Exception:
        ins = []
    for i in ins:
        walk(m, i, d + 1, seen)

for path in ('/Game/DeformableSnow/Material/MF_WorldToSnowUV',
             '/Game/DeformableSnow/Material/MF_CurrentToPrevious'):
    mf = unreal.load_asset(path)
    print('=' * 70)
    print('FUNCTION', path)
    exprs = None
    for prop in ('function_expressions', 'expressions'):
        try:
            exprs = list(mf.get_editor_property(prop)); print(' (via %s)' % prop); break
        except Exception as e:
            pass
    if exprs is None:
        print('  cannot enumerate expressions:', [a for a in dir(mf) if 'expr' in a.lower()])
        continue
    seen = set()
    for e in exprs:
        cls = e.get_class().get_name()
        if 'FunctionOutput' in cls:
            extra = ''
            try: extra = 'out=%s' % e.get_editor_property('output_name')
            except Exception: pass
            print(' ROOT %s %s' % (cls, extra))
            walk(mf, e, 1, seen)
