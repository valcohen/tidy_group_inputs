
# Tidy Group Inputs

A small addon to clean up Group Input nodes. It can hide all unlinked output sockets, and apply a custom color to all Group Input nodes. Works in any node editor in Blender 2.83+.

## Installation

Download the addon file and [install it as usual](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html). 

## Demo

When working with node groups, especially Geometry Nodes, I like to use many copies of the Group Input node, rather than linking a single giant Group Input to nodes all over the tree. This approach is encouraged (Blender developer Jacques Lucke [mentioned it here](https://twitter.com/JacquesLucke/status/1472263427477454856)) but Blender doesn't make it easy to keep the Group Inputs small. You can hide unused sockets with Ctrl-H, but as soon as you add a new input, Blender displays it in *all* the Group Input nodes in the current group. The nice tidy nodes get untidy quickly.

I was spending a lot of time hiding the new socket in all the Group Input nodes, so I thought I'd create a workaround. This addon sits in the Group tab in the Sidebar. When your Group Inputs start to get messy, just click the Hide Unused Sockets button:

![tidy](https://user-images.githubusercontent.com/8185037/170897483-b385c52e-1ef9-471d-ad69-aa8e1cf0aa73.gif)

## Usage

All settings are saved to the addon's preferences, rather than the current Blend file, so they become the default for all future use on any file. Most settings are exposed in both the Sidebar and Preferences panels.

The addon's operations change all the Group Input nodes in the currently-edited node tree. They don't affect nested Group Inputs -- you have to open and tidy each node tree separately.

The current node tree is named at the top of the addon panel.

Below that, `Hide Unused Sockets` hides output sockets without any links in all Group Input nodes. If `Incl. Unnamed Socket` is checked, the hide action also includes the unnamed output socket Blender automatically adds to Group Inputs.

In Preferences, you can `Enable Show All Button` to display a `Show All` button that will reverse the effect, i.e. it will show all sockets on all Group Inputs. This was slightly useful during development, and is mostly there to help tamp down the compulsion to have symmetrical actions. It's disabled by default.

The `Apply Color` button applies the custom color setting implied by the **Color** checkbox. If `Color` is checked, then `Apply Color` will set the Use Custom Color property on all Group Inputs and set their color to the one selected in the addon. If `Color` is unchecked, then `Apply Color` will unset the Use Custom Color property on all Group Inputs.

