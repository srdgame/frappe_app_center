editSnippets = function() {
    var sp = env.split;
    if (sp.getSplits() == 2) {
        sp.setSplits(1);
        return;
    }
    sp.setSplits(1);
    sp.setSplits(2);
    sp.setOrientation(sp.BESIDE);
    var editor = sp.$editors[1];
    var id = sp.$editors[0].session.$mode.$id || "";
    var m = snippetManager.files[id];
    if (!doclist["snippets/" + id]) {
        var text = m.snippetText;
        var s = doclist.initDoc(text, "", {});
        s.setMode("ace/mode/snippets");
        doclist["snippets/" + id] = s;
    }
    editor.on("blur", function() {
        m.snippetText = editor.getValue();
        snippetManager.unregister(m.snippets);
        m.snippets = snippetManager.parseSnippetFile(m.snippetText, m.scope);
        snippetManager.register(m.snippets);
    });
    sp.$editors[0].once("changeMode", function() {
        sp.setSplits(1);
    });
    editor.setSession(doclist["snippets/" + id], 1);
    editor.focus();
};


$(document).ready(function() {
	$(window).resize(function () {
		var h = Math.max($(window).height() - 130, 420);
		$('#editor_container, #editor_data, #jstree_tree, #editor_data .content').height(h).filter('.default').css('lineHeight', h + 'px');
		$('#jstree_tree_menu').width($('#jstree_tree').width())
	}).resize();


	var editorMode = {
		'txt': 'text',
		'md': 'markdown',
		'htaccess': 'text',
		'log': 'text',
		'js': 'javascript',
		'py': 'python',
		'c': 'c_cpp',
		'cpp': 'c_cpp',
		'cxx': 'c_cpp',
		'h': 'c_cpp',
		'hpp': 'c_cpp',
	};
    var code_editor = ace.edit("editor_code");
    //code_editor.setTheme("ace/theme/twilight");
    code_editor.session.setMode("ace/mode/lua");
    var local_storage_file = "{{ doc.name }}_saved_file:";
    var doc_list = {};

	var has_local_document = false;
	var editor_title_btn = $('#editor_menu .disabled.item.title');
    var refresh_editor_title = function() {
		var session = code_editor.session;
		editor_title_btn.html('<b>' + session.title + '</b>')
		if (has_local_document) {
			$('#/_anchor')
		}
	};

	var commands = code_editor.commands;
	commands.addCommand({
		name: "save",
		bindKey: {win: "Ctrl-S", mac: "Command-S"},
		exec: function(arg) {
			var session = code_editor.session;
			var name = session.name;
			localStorage.setItem(
				local_storage_file + name,
				session.getValue()
			);
			session.title = name + " *";
			refresh_editor_title();
			//code_editor.cmdLine.setValue("saved "+ name);
		}
	});
	commands.addCommand({
		name: "load",
		bindKey: {win: "Ctrl-O", mac: "Command-O"},
		exec: function(arg) {
			var session = code_editor.session;
			var name = session.name;
			var value = localStorage.getItem(local_storage_file + name);
			if (typeof value == "string") {
				session.setValue(value);
				//code_editor.cmdLine.setValue("loaded "+ name);
			} else {
				//code_editor.cmdLine.setValue("no previuos value saved for "+ name);
			}
		}
	});
	var editor_switch_document = function(doc_name, data) {
		var mode = editorMode[data.type];
		if (!mode) {
			mode = data.type;
		}
		var s = doc_list[doc_name];
		if (!s) {
			var name = doc_name;
			var value = localStorage.getItem(local_storage_file + name);
			if (typeof value == "string") {
				s = ace.createEditSession(value, "ace/mode/" + mode);
				s.title = doc_name + " *";
				//code_editor.cmdLine.setValue("loaded "+ name);
			} else {
				s = ace.createEditSession(data.content, "ace/mode/" + mode);
				s.title = doc_name;
			}
			s.name = name;
			doc_list[name] = s;
		}
		code_editor.setSession(s, 1);
		code_editor.focus();
		refresh_editor_title();
	};

	var backend_url = '/api/method/app_center.appmgr.editor?app={{ doc.name }}';
	var selected_file = null;
	$('#jstree_tree').jstree({
		'core' : {
			'data' : {
				'url' : backend_url,
				'data' : function (node) {
					return { 'operation': 'get_node', 'id' : node.id };
				}
			},
			'check_callback' : function(o, n, p, i, m) {
				if(m && m.dnd && m.pos !== 'i') { return false; }
				if(o === "move_node" || o === "copy_node") {
					if(this.get_node(n).parent === this.get_node(p).id) { return false; }
				}
				return true;
			},
			'themes' : {
				'responsive' : false,
				'variant' : 'small',
				'stripes' : true
			}
		},
		'sort' : function(a, b) {
			return this.get_type(a) === this.get_type(b) ? (this.get_text(a) > this.get_text(b) ? 1 : -1) : (this.get_type(a) >= this.get_type(b) ? 1 : -1);
		},
		'contextmenu' : {
			'items' : function(node) {
				var tmp = $.jstree.defaults.contextmenu.items();
				delete tmp.create.action;
				tmp.create.label = "New";
				tmp.create.submenu = {
					"create_folder" : {
						"separator_after"	: true,
						"label"				: "Folder",
						"action"			: function (data) {
							var inst = $.jstree.reference(data.reference),
								obj = inst.get_node(data.reference);
							inst.create_node(obj, { type : "default" }, "last", function (new_node) {
								setTimeout(function () { inst.edit(new_node); },0);
							});
						}
					},
					"create_file" : {
						"label"				: "File",
						"action"			: function (data) {
							var inst = $.jstree.reference(data.reference),
								obj = inst.get_node(data.reference);
							inst.create_node(obj, { type : "file" }, "last", function (new_node) {
								setTimeout(function () { inst.edit(new_node); },0);
							});
						}
					}
				};
				if(this.get_type(node) === "file") {
					delete tmp.create;
				}
				return tmp;
			}
		},
		'types' : {
			'default' : { 'icon' : 'folder' },
			'file' : { 'valid_children' : [], 'icon' : 'file' }
		},
		'unique' : {
			'duplicate' : function (name, counter) {
				return name + ' ' + counter;
			}
		},
		'plugins' : ['state','dnd','sort','types','contextmenu','unique',"wholerow"]
	})
	.on('delete_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'delete_node', 'id' : data.node.id })
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('create_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'create_node', 'type' : data.node.type, 'id' : data.node.parent, 'text' : data.node.text })
			.done(function (d) {
				data.instance.set_id(data.node, d.id);
				if (d.icon) {
					data.instance.set_icon(data.node, d.icon);
				}
			})
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('rename_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'rename_node', 'id' : data.node.id, 'text' : data.text })
			.done(function (d) {
				data.instance.set_id(data.node, d.id);
				if (d.icon) {
					data.instance.set_icon(data.node, d.icon);
				}
			})
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('move_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'move_node', 'id' : data.node.id, 'parent' : data.parent })
			.done(function (d) {
				//data.instance.load_node(data.parent);
				data.instance.refresh();
			})
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('copy_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'copy_node', 'id' : data.original.id, 'parent' : data.parent })
			.done(function (d) {
				//data.instance.load_node(data.parent);
				data.instance.refresh();
			})
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('changed.jstree', function (e, data) {
		if(data && data.selected && data.selected.length) {
			var new_selected_file = data.selected.join(':');
			if (selected_file == new_selected_file) {
				$('#editor_data .code').show();
				return;
			} else {
			}
			if (data.node.type == 'default') {
				return;
			}
			$.get(backend_url+'&operation=get_content&id=' + data.selected.join(':'), function (d) {
				if(d && typeof d.type !== 'undefined') {
					$('#editor_data .content').hide();
					switch(d.type) {
						case 'text':
						case 'txt':
						case 'md':
						case 'htaccess':
						case 'log':
						case 'sql':
						case 'php':
						case 'js':
						case 'json':
						case 'css':
						case 'html':
						case 'lua':
						case 'py':
						case 'c':
						case 'cpp':
						case 'cxx':
						case 'h':
						case 'hpp':
							$('#editor_data .code').show();
							selected_file = new_selected_file;
							editor_switch_document(selected_file, d);
							break;
						case 'png':
						case 'jpg':
						case 'jpeg':
						case 'bmp':
						case 'gif':
							$('#editor_data .image img').one('load', function () { $(this).css({'marginTop':'-' + $(this).height()/2 + 'px','marginLeft':'-' + $(this).width()/2 + 'px'}); }).attr('src',d.content);
							$('#editor_data .image').show();
							break;
						default:
							$('#editor_data .default').html(d.content).show();
							break;
					}
				}
			});
		}
		else {
			$('#editor_data .content').hide();
			$('#editor_data .default').html('Select a file from the tree.').show();
		}
	});

	var jstree_create_file = function() {
		var ref = $('#jstree_tree').jstree(true),
			sel = ref.get_selected();
		if(!sel.length) { return false; }
		sel = sel[0];
		sel = ref.create_node(sel, {"type":"file"});
		if(sel) {
			ref.edit(sel);
		}
	};
	var jstree_create_folder = function() {
		var ref = $('#jstree_tree').jstree(true),
			sel = ref.get_selected();
		if(!sel.length) { return false; }
		sel = sel[0];
		sel = ref.create_node(sel, {"type":"default"});
		if(sel) {
			ref.edit(sel);
		}
	};
	var jstree_rename = function() {
		var ref = $('#jstree_tree').jstree(true),
			sel = ref.get_selected();
		if(!sel.length) { return false; }
		sel = sel[0];
		ref.edit(sel);
	};
	var jstree_delete = function() {
		var ref = $('#jstree_tree').jstree(true),
			sel = ref.get_selected();
		if(!sel.length) { return false; }
		ref.delete_node(sel);
	};

	$('#jstree_tree_menu .item.file').click(jstree_create_file);
	$('#jstree_tree_menu .item.folder').click(jstree_create_folder);
	$('#jstree_tree_menu .item.rename').click(jstree_rename);
	$('#jstree_tree_menu .item.delete').click(jstree_delete);

	$('#editor_menu .item.save').click(function () {
		// var backend_url = '/api/method/app_center.appmgr.editor';
		// var args = {
		// 	'app': '{{ doc.name }}',
		// 	'operation': 'set_content',
		// 	'id' : selected_file,
		// 	'text' : code_editor.getValue()
		// };
		// $.post(backend_url, args)
		// 	.done(function (d) {
		// 		alert('Saved');
		// 	})
		// 	.fail(function () {
		// 		alert('Save Failed!');
		// 	});
		code_editor.execCommand('save', {});
	});
});