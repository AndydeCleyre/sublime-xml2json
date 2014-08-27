import sublime, sublime_plugin

if sublime.version() >= '3000':
	from collections import OrderedDict
	import json
	from . import xmltodict
else:
	import xmltodict
	import simplejson as json
	from ordereddict import OrderedDict

def newViewWithText(text):
	newView = sublime.active_window().new_file()
	if sublime.version() >= '3000':
		newView.run_command('append',{'characters':text})
	else:
		newEdit = newView.begin_edit()
		newView.insert(newEdit,0,text)
		newView.end_edit(newEdit)
class Xml2jsonCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		fulltext = self.view.substr(sublime.Region(0, self.view.size()))
		try:
			jsonObj = xmltodict.parse(fulltext)
			jsonStr = json.dumps(jsonObj)
		except Exception as e:
			sublime.error_message('xml2json error: ' + e.message)
			return
		newViewWithText(jsonStr)
		
class Json2xmlCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		fulltext = self.view.substr(sublime.Region(0, self.view.size()))
		try:
			jsonObj = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(fulltext)
			xmlStr = xmltodict.unparse(jsonObj)
		except ValueError:
			try:
				newText = '{"root":' + fulltext + '}' #try to add a wrapper
				jsonObj = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(fulltext)
				xmlStr = xmltodict.unparse(jsonObj)
			except Exception as e:
				newViewWithText(newText)
				sublime.error_message('json2xml error!!: ' + e.message)
				return
		except Exception as e:
			sublime.error_message('json2xml error: ' + e.message)
			return
		newViewWithText(xmlStr)
