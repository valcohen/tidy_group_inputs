bl_info = {
    "name": "Tidy Group Inputs",
    "description": "Collapse the Group Input nodes that Blender expands every time you add an input.",
    "author": "vbc",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "location": "Node Editor > N Panel > Group",
    "category": "Node",
}

import bpy

# UI Panel
class VBC_PT_tidy_group_inputs_panel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = 'Tidy Group Inputs'
    bl_category = 'Group' # tab name, can use existing e.g. 'View'
    
    def draw(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        layout = self.layout
                
        layout.label(text = f"Group: '{context.space_data.edit_tree.name}'")
        
        hide_box = layout.box()
        
        row = hide_box.row(align=True) #------------- HIDE ALL ACTION BUTTTON
        row.operator('vbc.hide_group_input_sockets', text="Hide Unused Sockets")
        
        row = hide_box.row(align=True) #------------- hide unnamed socket
        row.prop(prefs, 'hide_unnamed_socket', text = "Incl. Unnamed Socket")

        if (prefs.enable_show_all):
            row = hide_box.row(align=True) #------------- SHOW ALL ACTION BUTTTON
            row.operator('vbc.show_group_input_sockets', text="Show All")
        
        layout.separator()
        
        color_box = layout.box()
        
        row = color_box.row(align=True) #------------- APPLY COLOR ACTION BUTTTON
        row.operator('vbc.set_group_input_color', text="Apply Color")
        
        row = color_box.row(align=True) #------------- custom color
        row.prop(prefs, 'use_custom_color', text = "Color:")    # checkbox
        row.prop(prefs, 'gi_custom_color',  text = "") # color picker

class HideUnusedOutputSocketsOp(bpy.types.Operator):
    bl_idname = 'vbc.hide_group_input_sockets'
    bl_label = "Hide Unused"
    bl_description = 'Hide all unlinked output sockets on each Group Input node in the current group' 
    bl_options = {'INTERNAL'}
    
    # check if we can run in the current context
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        touched = 0

        gi_nodes = get_group_input_nodes(context.space_data.edit_tree) # currently edited node group
        for node in gi_nodes:
            for socket in node.outputs:
                has_link = len(socket.links) > 0
                has_name = len(socket.name) > 0

                if not has_link and ( has_name or prefs.hide_unnamed_socket ):
                    socket.hide = True
                    touched += 1

        # self.report({'INFO'}, f"Hid {touched} sockets on {len(gi_nodes)} Group Input nodes")        
        return {'FINISHED'}

class ShowAllOutputSocketsOp(bpy.types.Operator):
    bl_idname = 'vbc.show_group_input_sockets'
    bl_label = "Show All"
    bl_description = 'Unhide all output sockets on each Group Input node in the current group' 
    bl_options = {'INTERNAL'}
    
    # check if we can run in the current context
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        touched = 0
        
        gi_nodes = get_group_input_nodes(context.space_data.edit_tree) # currently edited node group
        for node in gi_nodes:
            for socket in node.outputs:
                socket.hide = False
                touched += 1

        # self.report({'INFO'}, f"Unhid {touched} sockets on {len(gi_nodes)} Group Input nodes")        
        return {'FINISHED'}

class SetGroupInputColorOp(bpy.types.Operator):
    bl_idname = 'vbc.set_group_input_color'
    bl_label = "Apply Color"
    bl_description = 'Set or unset the custom color on each Group Input node in the current group' 
    bl_options = {'INTERNAL'}
    
    # check if we can run in the current context
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        custom_color = prefs.gi_custom_color
        
        gi_nodes = get_group_input_nodes(context.space_data.edit_tree) # currently edited node group
        for node in gi_nodes:
            if prefs.use_custom_color:
                node.color = custom_color
                node.use_custom_color = True
            else:
                node.use_custom_color = False
                            
        status = 'Set' if prefs.use_custom_color else 'Unset'
        # self.report({'INFO'}, f"{status} custom color on {len(gi_nodes)} Group Input nodes")        
        return {'FINISHED'}

def get_group_input_nodes(current_group):
    return list(filter(lambda x: "GROUP_INPUT" in x.type, current_group.nodes))

class TidyGroupInputPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    hide_unnamed_socket: bpy.props.BoolProperty ( \
        name = "Hide Unnamed Socket",
        description = "Also hide the empty unnamed socket that Blender appends to each Group Input node",
        default = True
    )

    enable_show_all: bpy.props.BoolProperty(
        name = "Enable Show All button",
        description = "Show the Show All button to display all output sockets on all Group Input nodes",
        default = False,
    )
    
    use_custom_color: bpy.props.BoolProperty ( \
        name = "Use Custom Color",
        description = "Use a custom color for Group Input nodes",
        default = False
    )

    gi_custom_color: bpy.props.FloatVectorProperty ( \
        name = "Default Custom Color",
        description = "Custom color for Group Input nodes",
        subtype = 'COLOR_GAMMA',
        min = 0, max = 1,
        default = [0.1,0.3,0.5]
    )


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "hide_unnamed_socket")
        layout.prop(self, "enable_show_all")

        row = layout.row(align=True)
        row.prop(self, 'use_custom_color', text = "Color:")    # checkbox
        row.prop(self, 'gi_custom_color',  text = "") # color picker

classes = (
    HideUnusedOutputSocketsOp, 
    ShowAllOutputSocketsOp,
    SetGroupInputColorOp,
    VBC_PT_tidy_group_inputs_panel,
    TidyGroupInputPreferences
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()