jQuery(function ($) {
    var download_button = $('#configuration-download');

    // Create a blob object.
    var bb = new Blob(
        ["---\naudit:\n  parameter_values: true\n  exclude_vector_patterns: []\n  include_vector_patterns: []\n  link_templates: []\n  links: true\n  forms: true\n  cookies: true\n  jsons: true\n  xmls: true\n  ui_forms: true\n  ui_inputs: true\nbrowser_cluster:\n  local_storage: {}\n  wait_for_elements: {}\n  pool_size: 6\n  job_timeout: 25\n  worker_time_to_live: 100\n  ignore_images: false\n  screen_width: 1600\n  screen_height: 1200\ndatastore:\n  report_path: \n  token: b6dd40ef18c8c0e60e516f82ddccd137\nhttp:\n  user_agent: Arachni/v1.4\n  request_timeout: 10000\n  request_redirect_limit: 5\n  request_concurrency: 20\n  request_queue_size: 100\n  request_headers: {}\n  response_max_size: 500000\n  cookies: {}\n  authentication_type: auto\ninput:\n  values:\n    name: arachni_name\n    user: arachni_user\n    usr: arachni_user\n    pass: 5543!%arachni_secret\n    txt: arachni_text\n    num: '132'\n    amount: '100'\n    mail: arachni@email.gr\n    account: '12'\n    id: '1'\n  default_values:\n    name: arachni_name\n    user: arachni_user\n    usr: arachni_user\n    pass: 5543!%arachni_secret\n    txt: arachni_text\n    num: '132'\n    amount: '100'\n    mail: arachni@email.gr\n    account: '12'\n    id: '1'\n  without_defaults: true\n  force: false\nscope:\n  redundant_path_patterns: {}\n  dom_depth_limit: 5\n  exclude_file_extensions: []\n  exclude_path_patterns: []\n  exclude_content_patterns: []\n  include_path_patterns: []\n  restrict_paths: []\n  extend_paths: []\n  url_rewrites: {}\nsession: {}\nchecks:\n- xss\n- xss_path\n- xss_tag\n- xss_script_context\n- xss_event\n- xss_dom\n- xss_dom_script_context\nplatforms: []\nplugins:\n  autothrottle: {}\n  discovery: {}\n  healthmap: {}\n  timing_attacks: {}\n  uniformity: {}\nno_fingerprinting: false\nauthorized_by: \nurl: http://testhtml5.vulnweb.com/\n"],
        { type : 'application/yaml' }
    );

    download_button.attr( 'href', window.URL.createObjectURL( bb ) );
    download_button.attr( 'download', 'testhtml5.vulnweb.com-profile.afp' );
});
