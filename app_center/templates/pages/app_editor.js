$(document).ready(function() {
	$(window).resize(function () {
		var h = Math.max($(window).height() - 160, 420);
		$('#editor_container, #editor_data, #jstree_tree, #editor_data .content').height(h).filter('.default').css('lineHeight', h + 'px');
		$('#jstree_tree_menu').width($('#jstree_tree').width());
	}).resize();

	var cur_app = "{{ doc.name }}";

	var editorMode = {
		'txt': 'text',
		'csv': 'text',
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
    code_editor.setTheme("ace/theme/tomorrow");
    code_editor.session.setMode("ace/mode/lua");
    code_editor.setOptions({
		enableBasicAutocompletion: true,
		enableSnippets: true,
		enableLiveAutocompletion: true
	});
    var local_storage_prefix = cur_app + "_saved_file:";
    var doc_list = {};

	var editor_title_item = $('#editor_menu .disabled.item.title').on('click', function() {
		$(this).removeClass('active');
	});
	code_editor.on("change", function(e) {
		var session = code_editor.getSession();
		session.changed = true;
		editor_title_item.html('<b>' + session.name + " ***" + '</b>');
		editor_title_item.removeClass('modified').addClass('modified');
		$('#jstree_tree_menu .item.upload').removeClass('disabled');
		$('#editor_menu .item.save').removeClass('disabled');
	});
	code_editor.on("blur", function() {
		var session = code_editor.getSession();
		if (session.changed) {
			code_editor.execCommand('save', {});
		}
	});
	code_editor.on("changeSession", function(e) {
		var session = code_editor.getSession();
		var title = session.name;
		editor_title_item.removeClass('modified');
		if (session.changed) {
			title = title + ' *';
			editor_title_item.addClass('modified');
		}
		editor_title_item.html('<b>' + title + '</b>');
		if (session.changed) {
			$('#jstree_tree_menu .item.upload').removeClass('disabled');
			$('#editor_menu .item.save').removeClass('disabled');
		} else {
			$('#editor_menu .item.save').addClass('disabled');
		}
	});

	var commands = code_editor.commands;
	commands.addCommand({
		name: "save",
		bindKey: {win: "Ctrl-S", mac: "Command-S"},
		exec: function(arg) {
			var session = code_editor.session;
			var name = session.name;
			localStorage.setItem(
				local_storage_prefix + name,
				session.getValue()
			);
			session.changed = true;
			editor_title_item.removeClass('modified').addClass('modified');
			editor_title_item.html('<b>' + session.name + " *" + '</b>');
			//code_editor.cmdLine.setValue("saved "+ name);
		}
	});
	commands.addCommand({
		name: "load",
		bindKey: {win: "Ctrl-O", mac: "Command-O"},
		exec: function(arg) {
			var session = code_editor.session;
			var name = session.name;
			var value = localStorage.getItem(local_storage_prefix + name);
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
			var value = localStorage.getItem(local_storage_prefix + name);
			if (typeof value == "string") {
				s = ace.createEditSession(value, "ace/mode/" + mode);
				s.changed = true;
				//code_editor.cmdLine.setValue("loaded "+ name);
			} else {
				s = ace.createEditSession(data.content, "ace/mode/" + mode);
			}
			s.name = name;
			doc_list[name] = s;
		}
		code_editor.setSession(s, 1);
		code_editor.focus();
	};
	var editor_rename_document = function(doc_name, data) {
		if (doc_name == data.id)
			return;
		var session = doc_list[doc_name];
		if (session) {
			session.name = data.id;
			doc_list[data.id] = session;
			doc_list[doc_name] = null;
			var type = selected_file.split('.').pop();
			var mode = editorMode[data.type];
			if (!mode) {
				mode = data.type;
			}
			session.setMode("ace/mode/" + mode);
		}
		var value = localStorage.getItem(local_storage_prefix + doc_name);
		if (typeof value == 'string') {
			localStorage.setItem(local_storage_prefix + data.id);
			localStorage.removeItem(local_storage_prefix + doc_name);
		}
	};

	var backend_url = '/api/method/app_center.editor.editor?app=' + cur_app;
	var get_file_content = function(doc_name) {
		$.get(backend_url+'&operation=get_content&id=' + doc_name, function (d) {
			if(d && typeof d.type !== 'undefined') {
				$('#editor_data .content').hide();
				switch(d.type) {
					case 'text':
					case 'txt':
					case 'csv':
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
						editor_switch_document(doc_name, d);
						break;
					case 'png':
					case 'jpg':
					case 'jpeg':
					case 'bmp':
					case 'gif':
						$('#editor_data .image img')
							.one('load', function () {
								$(this).css({
									'marginTop':'-' + $(this).height()/2 + 'px',
									'marginLeft':'-' + $(this).width()/2 + 'px'
								});
							})
							.attr('src',d.content)
						;
						$('#editor_data .image').show();
						break;
					default:
						$('#editor_data .default').html(d.content).show();
						break;
				}
			}
		});
	};
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
				var doc_name = data.node.id;
				data.instance.set_id(data.node, d.id);
				if (d.icon) {
					data.instance.set_icon(data.node, d.icon);
				}
				editor_rename_document(doc_name, d.id);
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
			if (data.node.type == 'default') {
				return;
			}
			var selected_file = data.selected.join(':');
			var session = doc_list[selected_file];
			if (session) {
				$('#editor_data .code').show();
				code_editor.setSession(session, 1);
				code_editor.focus();
			} else {
				var value = localStorage.getItem(local_storage_prefix + selected_file);
				if (typeof value == "string") {
					var type = selected_file.split('.').pop();
					editor_switch_document(selected_file, {"type": type, "content": value});
				} else {
					get_file_content(selected_file);
				}
			}
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

	$('.ui.new_tag.form, .ui.apply_device.form').form({
		fields: {
			device : 'empty',
			version : 'integer',
			comment : ['minLength[10]', 'empty'],
			terms : 'checked'
		}
	});
	$('.ui.new_tag.form').ajaxForm({
		dataType: 'json',
		resetForm: true,
		beforeSend: function () {
			$('.ui.new_tag.form').removeClass('success').removeClass('error');
		},
		success: function (response) {
			$('.ui.new_tag.form .ui.success.message').html(response.message);
			$('.ui.new_tag.form').addClass('success');
			setTimeout(function () {
				$('.ui.new_tag.modal').modal('hide');
			}, 1000);
		},
		error: function(xhr) {
			$('.ui.new_tag.form').addClass('error');
			console.log('Tag Application Exception:' + xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				$('.ui.new_tag.form .ui.error.message').html(xhr.responseJSON._server_messages);
			} else {
				$('.ui.new_tag.form .ui.error.message').html('Revert Application Failed!');
			}
		}
	});
	$('.ui.new_tag.form .cancel.button').click(function(){
		$('.ui.new_tag.modal').modal('hide');
	});

	$('.ui.apply_device.form').ajaxForm({
		dataType: 'json',
		resetForm: true,
		beforeSend: function () {
			$('.ui.apply_device.form').removeClass('success').removeClass('error');
		},
		success: function (response) {
			$('.ui.apply_device.form .ui.success.message').html(response.message);
			$('.ui.apply_device.form').addClass('success');
			setTimeout(function () {
				$('.ui.apply_device.modal').modal('hide');
			}, 1000);
		},
		error: function(xhr) {
			$('.ui.apply_device.form').addClass('error');
			console.log('Release Application Exception:' + xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				$('.ui.apply_device.form .ui.error.message').html(xhr.responseJSON._server_messages);
			} else {
				$('.ui.apply_device.form .ui.error.message').html('Revert Application Failed!');
			}
		}
	});
	$('.ui.apply_device.form .cancel.button').click(function(){
		$('.ui.apply_device.modal').modal('hide');
	});

	$('.ui.revert_app.form').form({
		fields: {
			version : 'integer',
		}
	});
	$('.ui.revert_app.form').ajaxForm({
		dataType: 'json',
		beforeSend: function () {
			$('.ui.revert_app.form').removeClass('success').removeClass('error');
		},
		success: function (response) {
			$('.ui.revert_app.form .ui.success.message').html(response.message);
			$('.ui.revert_app.form').addClass('success');
			for (var name in doc_list) {
				localStorage.removeItem(local_storage_prefix + name);
			}
			setTimeout(function () {
				//window.location.href="/app_editor?app=" + cur_app;
				window.location.reload();
			}, 1000);
		},
		error: function(xhr) {
			$('.ui.revert_app.form').addClass('error');
			console.log('Revert Application Exception:' + xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				$('.ui.revert_app.form .ui.error.message').html(xhr.responseJSON._server_messages);
			} else {
				$('.ui.revert_app.form .ui.error.message').html('Revert Application Failed!');
			}
		}
	});
	$('.ui.revert_app.form .cancel.button').click(function(){
		$('.ui.revert_app.modal').modal('hide');
	});

	var upload_application_file = function(name, content) {
		var backend_url = '/api/method/app_center.editor.editor';
		var args = {
			'app': cur_app,
			'operation': 'set_content',
			'id' : name,
			'text' : content,
		};
		$.post(backend_url, args)
			.done(function (d) {
				var session = doc_list[name];
				session.changed = false;
				localStorage.removeItem(local_storage_prefix + name);
				if (code_editor.getSession() == session) {
					editor_title_item.removeClass('modified');
					editor_title_item.html('<b>' + session.name + '</b>');
				}
			})
			.fail(function () {
				var session = doc_list[name];
				code_editor.setSession(session, 1);
				code_editor.focus();
				$('#jstree_tree_menu .item.upload').removeClass('disabled');
				alert("Upload Failed!");
			});
	};
	var apply_application = function() {
		$('.ui.apply_device.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	};
	var tag_application = function() {
		$('.ui.new_tag.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	};
	var upload_application = function() {
		$('#jstree_tree_menu .item.upload').addClass('disabled');
		for (var name in doc_list) {
			var session = doc_list[name];
			if (session.changed) {
				upload_application_file(session.name, session.getValue())
			}
		}
	};
	var revert_application = function() {
		$('.ui.revert_app.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	};

	$('#jstree_tree_menu .item.tag').click(tag_application);
	$('#jstree_tree_menu .item.apply').click(apply_application);
	$('#jstree_tree_menu .item.upload').click(upload_application);
	$('#jstree_tree_menu .item.revert').click(revert_application);
	$('#jstree_tree_menu .item.file').click(jstree_create_file);
	$('#jstree_tree_menu .item.folder').click(jstree_create_folder);
	$('#jstree_tree_menu .item.rename').click(jstree_rename);
	$('#jstree_tree_menu .item.delete').click(jstree_delete);

	$('#editor_menu .item.save').click(function () {
		var session = code_editor.getSession();
		if (session.changed) {
			$('#editor_menu .item.save').addClass('disabled');
			upload_application_file(session.name, session.getValue());
		}
	});
	$('#editor_menu .item.download').click(function () {
		$('.ui.revert_file.modal')
			.modal({
				closable  : false,
				onApprove : function() {
					var session = code_editor.getSession();
					if (session.changed) {
						$('#editor_menu .item.save').addClass('disabled');
						localStorage.removeItem(local_storage_prefix + session.name);
						doc_list[session.name] = null;
						get_file_content(session.name);
					}
				}
			})
			.modal('show')
		;
	});
	$('#editor_menu .item.undo').click(function () {
		code_editor.undo();
	});
	$('#editor_menu .item.redo').click(function () {
		code_editor.redo();
	});

	$('#editor_menu .item.zoom').click(function () {
		var font_size = code_editor.getFontSize() + 1;
		code_editor.setFontSize(font_size);
	});
	$('#editor_menu .item.zoom_out').click(function () {
		var font_size = code_editor.getFontSize() - 1;
		code_editor.setFontSize(font_size);
	});
	$('#editor_menu .item.align_justify').click(function () {
		//code_editor.indent();
	});
});