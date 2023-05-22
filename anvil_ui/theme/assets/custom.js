function set_inner_html(id, html) {
  var el = anvil.js.get_dom_node(id);
  if (el) {
    el.innerHTML = html;
  }
}
