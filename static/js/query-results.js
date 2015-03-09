(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['query-results'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function";
  return "        <tr>\n          <td>\n            <div class=\"badge "
    + escapeExpression(((helpers.badge || (depth0 && depth0.badge) || helperMissing).call(depth0, (depth0 != null ? depth0.rating : depth0), {"name":"badge","hash":{},"data":data})))
    + "\"></div>\n          </td>\n          <td class=\"centered\" style=\"width: 250px;\">\n            <span class=\"beer-name\">"
    + escapeExpression(((helper = (helper = helpers.brewery || (depth0 != null ? depth0.brewery : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"brewery","hash":{},"data":data}) : helper)))
    + " "
    + escapeExpression(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"name","hash":{},"data":data}) : helper)))
    + "</span>  \n          </td>\n        </tr>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"row\">\n  <table style=\"margin: 0 auto;\">\n    <thead></thead>\n    <tbody>\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.results : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </tbody>\n  </table>\n</div>";
},"useData":true});
})();