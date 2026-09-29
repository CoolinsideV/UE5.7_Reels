# @Description: inspect snow setup
import unreal

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
for a in actors:
    cn = a.get_class().get_name()
    if cn in ('BP_Board_C','StaticMeshActor'):
        print('ACTOR %-16s class=%s label=%s' % (a.get_name(), cn, a.get_actor_label()))
        if cn == 'BP_Board_C':
            for v in ('Position','Size','PrePosition','MPC'):
                try:
                    print('    %-12s = %s' % (v, a.get_editor_property(v)))
                except Exception as e:
                    print('    %-12s ERR %s' % (v, e))
            try:
                comps = a.get_components_by_class(unreal.StaticMeshComponent)
                for c in comps:
                    print('    SMC %s mesh=%s scale=%s loc=%s' % (c.get_name(), c.get_editor_property('static_mesh'), c.get_editor_property('relative_scale3d'), c.get_editor_property('relative_location')))
            except Exception as e:
                print('    comps ERR', e)
        else:
            try:
                sm = a.static_mesh_component
                print('    mesh=%s' % sm.get_editor_property('static_mesh'))
                for i,m in enumerate(sm.get_editor_property('override_materials')):
                    print('    slot%d = %s' % (i, m))
            except Exception as e:
                print('    ERR', e)

for rt in ('/Game/DeformableSnow/Texture/RT_Snow','/Game/DeformableSnow/Texture/RT_SnowSave'):
    try:
        r = unreal.load_asset(rt)
        print('RT %s size=%sx%s fmt=%s flags=%s' % (rt, r.get_editor_property('size_x'), r.get_editor_property('size_y'),
              r.get_editor_property('render_target_format'), r.get_editor_property('target_gamma')))
    except Exception as e:
        print('RT %s ERR %s' % (rt, e))

mel = unreal.MaterialEditingLibrary
for mp in ('/Game/DeformableSnow/Material/MT_Snow','/Game/DeformableSnow/Material/MT_PingYi','/Game/DeformableSnow/Material/MT_Debug'):
    m = unreal.load_asset(mp)
    print('MAT %s blend=%s shading=%s twoSided=%s' % (mp, m.get_editor_property('blend_mode'), m.get_editor_property('shading_model'), m.get_editor_property('two_sided')))
    try:
        exprs = mel.get_material_expressions(m)
        print('   expressions(%d): %s' % (len(exprs), sorted(set(e.get_class().get_name() for e in exprs))))
    except Exception as e:
        print('   expr ERR', e)
    for prop in ('MP_BASE_COLOR','MP_WORLD_POSITION_OFFSET','MP_NORMAL','MP_EMISSIVE_COLOR','MP_ROUGHNESS','MP_METALLIC','MP_OPACITY','MP_SPECULAR'):
        try:
            node = mel.get_material_property_input_node(m, getattr(unreal.MaterialProperty, prop))
            print('   %-24s -> %s' % (prop, node.get_class().get_name() if node else 'NOT CONNECTED'))
        except Exception as e:
            print('   %-24s ERR %s' % (prop, e))
