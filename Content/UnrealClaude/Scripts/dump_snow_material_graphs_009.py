# @Description: dump snow material graphs
import unreal
mel = unreal.MaterialEditingLibrary

def walk(m, e, d, seen):
    k = e.get_path_name()
    if k in seen or d > 12: return
    seen.add(k)
    cls = e.get_class().get_name()
    extra = ''
    try:
        if 'CollectionParameter' in cls:
            extra = 'param=%s coll=%s' % (e.get_editor_property('parameter_name'), e.get_editor_property('collection'))
        elif 'TextureSample' in cls:
            extra = 'tex=%s' % e.get_editor_property('texture')
        elif cls == 'MaterialExpressionTextureObject':
            extra = 'tex=%s' % e.get_editor_property('texture')
        elif 'VectorParameter' in cls:
            extra = 'param=%s' % e.get_editor_property('parameter_name')
        elif 'ScalarParameter' in cls:
            extra = 'param=%s' % e.get_editor_property('parameter_name')
        elif 'Constant' in cls:
            extra = 'r=%s' % e.get_editor_property('r')
        elif 'FunctionCall' in cls:
            extra = 'func=%s' % e.get_editor_property('material_function')
        elif 'Custom' in cls:
            extra = 'code=%s' % str(e.get_editor_property('code'))[:200]
    except Exception as ex:
        extra = '(<%s>)' % ex
    print('  ' * d + cls + '   ' + extra)
    try:
        ins = list(mel.get_inputs_for_material_expression(m, e))
    except Exception:
        ins = []
    for i in ins:
        walk(m, i, d + 1, seen)

for path in ('/Game/DeformableSnow/Material/MT_Snow', '/Game/DeformableSnow/Material/MT_PingYi'):
    m = unreal.load_asset(path)
    print('=' * 70)
    print('MATERIAL', path, '| blend=', m.get_editor_property('blend_mode'), '| shading=', m.get_editor_property('shading_model'))
    try:
        print(' USED TEXTURES:', [t.get_path_name() for t in mel.get_used_textures(m)])
    except Exception as e:
        print(' usedtex err', e)
    for fn, lbl in ((mel.get_vector_parameter_names, 'VEC'), (mel.get_scalar_parameter_names, 'SCA'), (mel.get_texture_parameter_names, 'TEX')):
        try: print(' %s PARAMS: %s' % (lbl, list(fn(m))))
        except Exception as e: print(' %s err %s' % (lbl, e))
    for prop in ('MP_BASE_COLOR', 'MP_EMISSIVE_COLOR', 'MP_OPACITY', 'MP_WORLD_POSITION_OFFSET',
                 'MP_NORMAL', 'MP_ROUGHNESS', 'MP_METALLIC', 'MP_SPECULAR', 'MP_AMBIENT_OCCLUSION'):
        try:
            n = mel.get_material_property_input_node(m, getattr(unreal.MaterialProperty, prop))
        except Exception:
            continue
        if n:
            print(' PROP %-24s -> %s' % (prop, n.get_class().get_name()))
            walk(m, n, 2, set())

mpc = unreal.load_asset('/Game/DeformableSnow/Material/MPC_Snow')
try:
    for p in mpc.get_editor_property('vector_parameters'):
        print('MPC VEC %s = %s' % (p.get_editor_property('parameter_name'), p.get_editor_property('default_value')))
    for p in mpc.get_editor_property('scalar_parameters'):
        print('MPC SCA %s = %s' % (p.get_editor_property('parameter_name'), p.get_editor_property('default_value')))
except Exception as e:
    print('MPC err', e)
