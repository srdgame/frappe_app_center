$(document).ready(function() {

	$(window).resize(function () {
		var h = Math.max($(window).height() - 100, 420);
		$('#editor_container, #editor_data, #jstree_tree, #editor_data .content').height(h).filter('.default').css('lineHeight', h + 'px');
	}).resize();

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/javascript");

	var backend_url = '/api/method/app_center.appmgr.editor?app={{ doc.name }}';
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
		'plugins' : ['state','dnd','sort','types','contextmenu','unique']
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
			})
			.fail(function () {
				data.instance.refresh();
			});
	})
	.on('rename_node.jstree', function (e, data) {
		$.get(backend_url, { 'operation': 'rename_node', 'id' : data.node.id, 'text' : data.text })
			.done(function (d) {
				data.instance.set_id(data.node, d.id);
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
							$('#editor_data .code').show();
							$('#editor_code').val(d.content);
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
});