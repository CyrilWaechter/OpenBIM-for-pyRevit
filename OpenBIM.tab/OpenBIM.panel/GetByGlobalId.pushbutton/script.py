# coding=utf8
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, ElementId

from pyrevit import script, forms, revit

logger = script.get_logger()
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

text_ids = forms.ask_for_string(
    default="GlobalId",
    prompt="Enter comma separated GlobalId eg. 2N4yNZJ_XDjPMRumXBulXA, 2N4yNZJ_XDjPMRumXBulXD",
    title="Select by GlobalId",
)

if text_ids:
    ifc_globalids = {
        ifc_globalid.strip(): ElementId(-1) for ifc_globalid in text_ids.split(",")
    }
    for element in (
        FilteredElementCollector(doc)
        .WhereElementIsNotElementType()
        .WhereElementIsViewIndependent()
        .ToElements()
    ):
        globalid_parameter = element.get_Parameter(BuiltInParameter.IFC_GUID)
        if not globalid_parameter:
            continue
        ifc_guid = globalid_parameter.AsString()
        for ifc_globalid in ifc_globalids.keys():
            if ifc_guid == ifc_globalid:
                ifc_globalids[ifc_globalid] = element

    output = script.get_output()
    output.set_width(300)

    all_elements_ids = []
    str_output = ""
    for idx, (ifc_globalid, element) in enumerate(ifc_globalids.items()):
        str_output += "\t{}: {} {} ({})\n".format(
            idx, output.linkify(element.Id), revit.query.get_name(element), ifc_globalid
        )
        all_elements_ids.append(element.Id)

    str_output = "{}\n{}".format(
        output.linkify(all_elements_ids, title="All Elements"), str_output
    )
    print(str_output)
