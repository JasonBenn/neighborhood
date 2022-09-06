select ev.id, ev.name, ev.when, hb.name as building_name
from houses_event ev
         join houses_building hb on ev.building_id = hb.id;

