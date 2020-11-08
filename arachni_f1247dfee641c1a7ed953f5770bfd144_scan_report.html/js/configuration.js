jQuery(function ($) {
    var download_button = $('#configuration-download');

    // Create a blob object.
    var bb = new Blob(
        ["---\naudit:\n  parameter_values: true\n  exclude_vector_patterns: []\n  include_vector_patterns: []\n  link_templates: []\nbrowser_cluster:\n  local_storage: {}\n  wait_for_elements: {}\n  pool_size: 6\n  job_timeout: 25\n  worker_time_to_live: 100\n  ignore_images: false\n  screen_width: 1600\n  screen_height: 1200\ndatastore:\n  report_path: \n  token: f1247dfee641c1a7ed953f5770bfd144\nhttp:\n  user_agent: Arachni/v2.0dev\n  request_timeout: 10000\n  request_redirect_limit: 5\n  request_concurrency: 20\n  request_queue_size: 100\n  request_headers: {}\n  response_max_size: 500000\n  cookies: {}\n  authentication_type: auto\ninput:\n  values: {}\n  default_values:\n    \"(?i-mx:pass)\": 5543!%arachni_secret\n    \"(?i-mx:name)\": arachni_name\n    \"(?i-mx:mail)\": arachni@email.gr\n    \"(?i-mx:amount)\": '100'\n    \"(?i-mx:usr)\": arachni_user\n    \"(?i-mx:id)\": '1'\n    \"(?i-mx:txt)\": arachni_text\n    \"(?i-mx:account)\": '12'\n    \"(?i-mx:user)\": arachni_user\n    \"(?i-mx:num)\": '132'\n  without_defaults: false\n  force: false\nscope:\n  redundant_path_patterns: {}\n  dom_depth_limit: 5\n  exclude_file_extensions: []\n  exclude_path_patterns: []\n  exclude_content_patterns: []\n  include_path_patterns: []\n  restrict_paths: []\n  extend_paths: []\n  url_rewrites: {}\nsession:\n  check_url: http://b3789e93786d.ngrok.io/admin\n  check_pattern: \"(?-mix:logout)\"\nchecks:\n- allowed_methods\n- backdoors\n- backup_directories\n- csrf\n- path_traversal\n- htaccess_limit\n- html_objects\n- http_only_cookies\n- http_put\n- insecure_client_access_policy\n- insecure_cookies\n- insecure_cors_policy\n- insecure_cross_domain_policy_access\n- insecure_cross_domain_policy_headers\n- interesting_responses\n- backup_files\nplatforms: []\nplugins:\n  uniformity: {}\n  autothrottle: {}\n  autologin:\n    url: http://b3789e93786d.ngrok.io/\n    check: logout\n    parameters: email=admin@admin.com&password=password\n  healthmap: {}\n  timing_attacks: {}\n  discovery: {}\nno_fingerprinting: false\nauthorized_by: \nurl: http://b3789e93786d.ngrok.io/\n"],
        { type : 'application/yaml' }
    );

    download_button.attr( 'href', window.URL.createObjectURL( bb ) );
    download_button.attr( 'download', 'b3789e93786d.ngrok.io-profile.afp' );
});
