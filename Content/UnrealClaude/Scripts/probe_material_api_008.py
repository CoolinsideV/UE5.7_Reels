# @Description: probe material api
import unreal
mel = unreal.MaterialEditingLibrary
print('MEL API:', [a for a in dir(mel) if not a.startswith('_')])
