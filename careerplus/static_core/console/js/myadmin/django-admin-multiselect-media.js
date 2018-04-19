jQuery.each($("select[multiple]"), function () {
  // "Locations" can be any label you want
  SelectFilter.init(this.id, this.name, 0, "/media/");
 });