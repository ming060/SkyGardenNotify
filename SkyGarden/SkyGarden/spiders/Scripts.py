#!/usr/bin/env python
# encoding: utf-8

LUA_SCRIPT = """
function wait_loading(splash, maxwait)
  if maxwait == nil then
      maxwait = 10
  end
  return splash:wait_for_resume(string.format([[
    function main(splash) {
      var maxwait = %s;
      var end = Date.now() + maxwait*1000;

      function check() {
        var loading_gone = document.querySelector('div.bb-loader.ng-scope.ng-hide');
        var is_loading_gone = loading_gone != null;
        var h2_hide = document.querySelector('h2.ng-binding.ng-hide');
        var is_h2_hide_gone = h2_hide == null;
        if(is_loading_gone && is_h2_hide_gone) {
          splash.resume('Element found');
        } else if(Date.now() >= end) {
          var err = 'Timeout waiting for element';
          splash.error(err);
        } else {
          setTimeout(check, 200);
        }
      }
      check();
    }
  ]], maxwait))
end

function main(splash, args)
  local get_date = splash:jsfunc([[
  function () {
    return new Date().getTime();
  }
  ]])
  local start_time = get_date()
  splash:go(args.url)
  wait_loading(splash, 60)
  local end_time = get_date()
  elapsed_time = (end_time - start_time)/1000
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
    elapsed_time = elapsed_time,
  }
end
"""