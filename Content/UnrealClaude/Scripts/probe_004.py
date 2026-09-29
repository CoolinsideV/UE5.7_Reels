# @Description: probe api
import unreal
print('LIB:', [a for a in dir(unreal.BlueprintEditorLibrary) if 'graph' in a.lower()])
bp = unreal.load_asset('/Game/DeformableSnow/BluePrint/BP_Board')
print('BP:', [a for a in dir(bp) if 'graph' in a.lower()])
print('BPALL:', [a for a in dir(bp) if not a.startswith('_')][:80])
