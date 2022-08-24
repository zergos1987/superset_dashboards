// CUSTOM SUPERSET SCRIPTS #################################################


// UTILS


let is_dashboard_reader_user;
let user_data;


function update_innertext(text_input, text_output) {
    // UTILS - update_innertext


    if(text_output === undefined) {text_output = text_input}
    
    if(text_input.includes('seconds ago')) {text_output = text_input.replace('seconds ago', 'секунд назад')} else { if(text_input.includes('an seconds ago')) {text_output = text_input.replace('an seconds ago', 'секунд назад') } }
    if(text_input.includes('minutes ago')) {text_output = text_input.replace('minutes ago', 'минут назад')} else { if(text_input.includes('an minutes ago')) {text_output = text_input.replace('an minutes ago', 'минут назад') } else { if(text_input.includes('a minute ago')) {text_output = text_input.replace('a minute ago', 'минут назад')} } }
    if(text_input.includes('hours ago')) {text_output = text_input.replace('hours ago', 'часов назад')} else { if(text_input.includes('an hour ago')) {text_output = text_input.replace('an hour ago', 'час назад') } { if(text_input.includes('a hour ago')) {text_output = text_input.replace('a hour ago', 'час назад')} } }
    if(text_input.includes('days ago')) {text_output = text_input.replace('days ago', 'дней назад')} else { if(text_input.includes('an day ago')) {text_output = text_input.replace('an day ago', 'день назад') } else { if(text_input.includes('a day ago')) {text_output = text_input.replace('a day ago', 'день назад')} } }
    if(text_input.includes('weeks ago')) {text_output = text_input.replace('weeks ago', 'недель назад')} else { if(text_input.includes('an week ago')) {text_output = text_input.replace('an week ago', 'неделю назад') } { if(text_input.includes('a week ago')) {text_output = text_input.replace('a week ago', 'неделю назад')} } }
    if(text_input.includes('mounths ago')) {text_output = text_input.replace('mounths ago', 'месяцев назад')} else { if(text_input.includes('an mounth ago')) {text_output = text_input.replace('an mounth ago', 'месяц назад')} { if(text_input.includes('a mounth ago')) {text_output = text_input.replace('a mounth ago', 'месяц назад')} } }
    if(text_input.includes('years ago')) {text_output = text_input.replace('years ago', 'лет назад')} else { if(text_input.includes('an year ago')) {text_output = text_input.replace('an year ago', 'год назад') } { if(text_input.includes('a year ago')) {text_output = text_input.replace('a year ago', 'год назад')} } }
    if(text_output.includes(' обновлено')) {text_output = text_output.replace(' обновлено', '');text_output = 'обновлено: ' + text_output;}
    if(text_output.includes('Unknown')) {text_output = text_output.replace('Unknown', '-');}
    if(text_output.includes('Viewed')) {text_output = text_output.replace('Viewed', 'Просмотрено: ');}
    if(text_output.includes('Ran')) {text_output = text_output.replace('Ran', 'Выполнено: ');}
    if(text_output.includes('SEE ALL CHARTS')) {text_output = text_output.replace('SEE ALL CHARTS', 'Смотреть все визуализации');}
    
    if(text_output.includes('APPLY FILTERS')) {text_output = text_output.replace('APPLY FILTERS', 'Применить фильтры');}
    if(text_output.includes('All filters')) {text_output = text_output.replace('All filters', 'Все фильтры');}
    if(text_output.includes('Filter sets')) {text_output = text_output.replace('Filter sets', 'Наборы фильтров');}
    if(text_output.includes('ADD/EDIT FILTERS')) {text_output = text_output.replace('ADD/EDIT FILTERS', 'Добавить/Редактировать Фильтры');}
    if(text_output.includes('options')) {text_output = text_output.replace('options', 'опциий');} else { if(text_output.includes('option')) {text_output = text_output.replace('option', 'опциий');} }
    
    if(text_output.includes('Scoping')) {text_output = text_output.replace('Scoping', 'Области');}
    if(text_output.includes('Column')) {text_output = text_output.replace('Column', 'Колонка');}
    if(text_output.includes('FILTER TYPE')) {text_output = text_output.replace('FILTER TYPE', 'Тип фильтра');}
    if(text_output.includes('RESTORE FILTER')) {text_output = text_output.replace('RESTORE FILTER', 'Восстановить фильтр');}
    if(text_output.includes('Sort filter values')) {text_output = text_output.replace('Sort filter values', 'Сортировать значения фильтра');}

    if(text_output.includes('now')) {text_output = text_output.replace('now', 'сейчас');}
    if(text_output.includes('No dashboards yet')) {text_output = text_output.replace('No dashboards yet', 'Пока нет дашбордов');}
    if(text_output.includes('DASHBOARD')) {text_output = text_output.replace('DASHBOARD', 'Дашборд');}

    if(text_input.includes('Thumbnails')) {text_output = text_input.replace('Thumbnails', 'Превью')}
    
    return text_output;
}


function GetUserProps() {
    // UTILS - Get user properties


    user_data = JSON.parse(document.querySelector('[data-bootstrap]').getAttribute('data-bootstrap'));
    if(user_data.user) {
        // 
        if (user_data.user.username === 'admin' && user_data.user.email === 'admin@superset.com') {
            is_dashboard_reader_user = false;
        } else {
            // Activate Dashboard_Reader user page properties if user_exists
            is_dashboard_reader_user = (!user_data.user.roles.hasOwnProperty('Dashboards_Creator') && user_data.user.roles.hasOwnProperty('Dashboards_Reader')) || false;
            // console.log(is_dashboard_reader_user)
            if (is_dashboard_reader_user) {
                if(document.getElementById('app')) {document.getElementById('app').classList.add("Dashboard_Reader")};
                if(document.getElementById('app-menu')) {document.getElementById('app-menu').classList.add("Dashboard_Reader")};
            }
        }
    } else {
        // Anonymous user
    } 
}


// MAIN SRC


function Update_each_03_seconds(is_dashboard_reader_user) {
    // MAIN SRC - Update_each_03_seconds


    let target_nodes, target_node, ele_svg, ele_g, ele_path;
    // Update for ROLE: Dashboard_Reader
    if (is_dashboard_reader_user) {
        if(window.location.href.includes('/superset/dashboard/')) {
            // console.log(is_dashboard_reader_user)
            let target_nodes = document.querySelectorAll('[data-test="view-query-menu-item"]');
            if(target_nodes.length > 0) {
                target_nodes.forEach((item, index) => {if(item.innerText === "Скопировать запрос") {item.parentNode.parentNode.remove()}})
            }
            target_nodes = document.querySelectorAll('.language-sql');
            if(target_nodes.length > 0) {
                target_nodes.forEach((item, index) => {if(item.innerText === "Скопировать запрос") {item.parentNode.parentNode.parentNode.remove()}})
            }
        }
    }
    // add on Dashboards page - main-menu-icons
    if(document.querySelectorAll(".sp_main_menu_icon_sql_queries").length === 0
        && (!document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"] > svg') || !document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"] > svg'))) { 
        target_nodes = document.querySelectorAll('header > div > div .css-188dvs4 .ant-menu-submenu-title > span:not(.anticon.css-tp6bb2), header > div > div .menu-188dvs4 .ant-menu-submenu-title > span:not(.anticon.menu-tp6bb2)');
        target_nodes.forEach((item, index) => {
            if(item.innerText === 'Лаборатория SQL' && document.querySelectorAll(".sp_main_menu_icon_sql_queries").length === 0) {
                item.parentNode.parentNode.setAttribute('sp_main_menu_icon', 'on');
                ele_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                ele_g = document.createElementNS('http://www.w3.org/2000/svg', "g");
                ele_path = document.createElementNS('http://www.w3.org/2000/svg', "path");

                ele_svg.setAttribute("viewBox", "0 0 115.28 122.88");
                ele_svg.setAttribute("class", "sp_main_menu_icon_sql_queries");
                ele_svg.setAttribute("style", "fill-rule: evenodd;clip-rule:evenodd;");
                ele_path.setAttribute("d", "M25.38,57h64.88V37.34H69.59c-2.17,0-5.19-1.17-6.62-2.6c-1.43-1.43-2.3-4.01-2.3-6.17V7.64l0,0H8.15 c-0.18,0-0.32,0.09-0.41,0.18C7.59,7.92,7.55,8.05,7.55,8.24v106.45c0,0.14,0.09,0.32,0.18,0.41c0.09,0.14,0.28,0.18,0.41,0.18 c22.78,0,58.09,0,81.51,0c0.18,0,0.17-0.09,0.27-0.18c0.14-0.09,0.33-0.28,0.33-0.41v-11.16H25.38c-4.14,0-7.56-3.4-7.56-7.56 V64.55C17.82,60.4,21.22,57,25.38,57L25.38,57z M29.57,83.94l7.12-0.45c0.15,1.15,0.47,2.03,0.94,2.63 c0.77,0.98,1.87,1.47,3.31,1.47c1.07,0,1.89-0.25,2.47-0.75c0.58-0.5,0.87-1.08,0.87-1.75c0-0.63-0.27-1.19-0.82-1.69 c-0.55-0.5-1.82-0.96-3.83-1.41c-3.29-0.73-5.62-1.72-7.03-2.94c-1.41-1.22-2.12-2.78-2.12-4.68c0-1.24,0.36-2.42,1.08-3.52 c0.72-1.11,1.81-1.98,3.26-2.61c1.45-0.63,3.44-0.95,5.96-0.95c3.1,0,5.46,0.58,7.09,1.73c1.63,1.15,2.59,2.99,2.9,5.51l-7.05,0.42 c-0.19-1.1-0.58-1.9-1.18-2.4c-0.6-0.5-1.43-0.75-2.49-0.75c-0.87,0-1.53,0.19-1.97,0.55c-0.44,0.37-0.66,0.82-0.66,1.35 c0,0.38,0.18,0.73,0.54,1.04c0.34,0.32,1.18,0.62,2.5,0.89c3.28,0.71,5.62,1.42,7.03,2.15c1.42,0.72,2.45,1.62,3.09,2.69 c0.64,1.07,0.97,2.26,0.97,3.59c0,1.55-0.43,2.99-1.29,4.3c-0.86,1.31-2.06,2.31-3.61,2.99c-1.54,0.68-3.48,1.02-5.83,1.02 c-4.12,0-6.98-0.8-8.57-2.38C30.68,88.41,29.78,86.39,29.57,83.94L29.57,83.94z M76.38,88.41c0.93,0.65,1.54,1.06,1.83,1.23 c0.42,0.24,1.01,0.53,1.73,0.85l-2.07,4.2c-1.04-0.51-2.08-1.11-3.11-1.81c-1.03-0.7-1.75-1.23-2.15-1.58 c-1.65,0.72-3.73,1.08-6.22,1.08c-3.69,0-6.6-0.96-8.73-2.88c-2.52-2.27-3.78-5.46-3.78-9.57c0-3.99,1.1-7.09,3.3-9.31 c2.2-2.21,5.27-3.32,9.23-3.32c4.03,0,7.13,1.08,9.32,3.24c2.19,2.16,3.29,5.25,3.29,9.27C79.02,83.4,78.14,86.26,76.38,88.41 L76.38,88.41z M70.63,84.56c0.6-1.07,0.9-2.67,0.9-4.79c0-2.45-0.46-4.19-1.37-5.24c-0.92-1.04-2.17-1.57-3.77-1.57 c-1.5,0-2.71,0.54-3.63,1.6c-0.93,1.07-1.39,2.74-1.39,5.01c0,2.65,0.45,4.51,1.36,5.57c0.91,1.07,2.15,1.6,3.73,1.6 c0.51,0,0.99-0.05,1.44-0.15c-0.63-0.61-1.63-1.18-2.99-1.72l1.17-2.69c0.67,0.12,1.19,0.27,1.55,0.45 c0.37,0.17,1.1,0.64,2.17,1.39C70.06,84.2,70.33,84.38,70.63,84.56L70.63,84.56z M82.55,67.71h7.49V86h11.72v5.96H82.55V67.71 L82.55,67.71z M97.79,57h9.93c4.16,0,7.56,3.41,7.56,7.56v31.42c0,4.15-3.41,7.56-7.56,7.56h-9.93v13.55c0,1.61-0.65,3.04-1.7,4.1 c-1.06,1.06-2.49,1.7-4.1,1.7c-29.44,0-56.59,0-86.18,0c-1.61,0-3.04-0.64-4.1-1.7c-1.06-1.06-1.7-2.49-1.7-4.1V5.85 c0-1.61,0.65-3.04,1.7-4.1c1.06-1.06,2.53-1.7,4.1-1.7h58.72C64.66,0,64.8,0,64.94,0c0.64,0,1.29,0.28,1.75,0.69h0.09 c0.09,0.05,0.14,0.09,0.23,0.18l29.99,30.36c0.51,0.51,0.88,1.2,0.88,1.98c0,0.23-0.05,0.41-0.09,0.65V57L97.79,57z M67.52,27.97 V8.94l21.43,21.7H70.19c-0.74,0-1.38-0.32-1.89-0.78C67.84,29.4,67.52,28.71,67.52,27.97L67.52,27.97z");
                ele_g.appendChild(ele_path);
                ele_svg.appendChild(ele_g);
                item.appendChild(ele_svg);
                console.log(item)
            }
        })
        // console.log(1)
    }

    if(document.querySelectorAll(".sp_main_menu_icon_bd").length === 0 
    && (!document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"] > svg') || !document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"] > svg'))) {
        target_nodes = document.querySelectorAll('header > div > div .css-188dvs4 .ant-menu-submenu-title > span:not(.anticon.css-tp6bb2), header > div > div .menu-188dvs4 .ant-menu-submenu-title > span:not(.anticon.menu-tp6bb2)');
        target_nodes.forEach((item, index) => {
            if(item.innerText === 'БД' && document.querySelectorAll(".sp_main_menu_icon_bd").length === 0) {
                item.parentNode.parentNode.setAttribute('sp_main_menu_icon', 'on');
                ele_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                ele_g = document.createElementNS('http://www.w3.org/2000/svg', "g");
                ele_path = document.createElementNS('http://www.w3.org/2000/svg', "path");
        
                ele_svg.setAttribute("viewBox", "0 0 122.88 116.41");
                ele_svg.setAttribute("class", "sp_main_menu_icon_bd");
                ele_svg.setAttribute("style", "fill-rule: evenodd;");
                ele_path.setAttribute("d", "M16.49,24.88C24.05,27.41,34.57,29,46.26,29S68.48,27.41,76,24.88c6.63-2.22,10.73-4.9,10.73-7.52S82.67,12.06,76,9.84C68.48,7.33,58,5.75,46.27,5.75S24.06,7.33,16.49,9.84c-14.06,4.7-14.46,10.21,0,15ZM64.91,55.34h48.73a9.27,9.27,0,0,1,9.24,9.24v42.58a9.27,9.27,0,0,1-9.24,9.25H64.91a9.27,9.27,0,0,1-9.24-9.25V64.58a9.27,9.27,0,0,1,9.24-9.24ZM91.09,99.18H118v12H91.09v-12Zm-30.89,0H87.13v12H60.2v-12Zm0-31.89H87.13v12H60.2v-12Zm0,15.94H87.13v12H60.2v-12ZM91.09,67.29H118v12H91.09v-12Zm0,15.94H118v12H91.09v-12ZM5.82,45.77c.52,2.45,4.5,4.91,10.68,7,7.22,2.42,17.16,3.95,28.24,4.08v5.77c-11.67-.13-22.25-1.78-30.05-4.39A35.86,35.86,0,0,1,5.84,54V71.27c.52,2.45,4.5,4.91,10.68,7,7.22,2.4,17.15,3.94,28.22,4.07v5.75c-11.67-.14-22.25-1.78-30.05-4.4A36.08,36.08,0,0,1,5.83,79.5V96.75c.52,2.45,4.51,4.91,10.68,7,7.22,2.41,17.16,4,28.23,4.08v5.75c-11.67-.13-22.24-1.78-30-4.4C10.4,107.72,0,103,0,97.38V95.55C0,69.86,0,43.06,0,17.41c0-5.43,5.61-10,14.66-13C22.82,1.68,34,0,46.27,0S69.7,1.68,77.87,4.41s13.64,6.78,14.55,11.53a3,3,0,0,1,.16,1v28.6H86.8V26.09a36.69,36.69,0,0,1-8.93,4.22c-8.15,2.75-19.31,4.41-31.58,4.41S22.83,33,14.66,30.31A36.26,36.26,0,0,1,5.8,26.14V45.77Z");
                ele_g.appendChild(ele_path);
                ele_svg.appendChild(ele_g);
                item.appendChild(ele_svg);
                console.log(item)
            }
        })
        // console.log(2)
    }

    if(document.querySelectorAll(".sp_main_menu_icon_settings").length === 0  
    && (!document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"] > svg') || !document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"] > svg'))) {
        target_nodes = document.querySelectorAll('header > div > div .css-188dvs4 .ant-menu-submenu-title > span:not(.anticon.css-tp6bb2), header > div > div .menu-188dvs4 .ant-menu-submenu-title > span:not(.anticon.menu-tp6bb2)');
        target_nodes.forEach((item, index) => {
            if(item.innerText === 'Настройки' && document.querySelectorAll(".sp_main_menu_icon_settings").length === 0) {
                item.parentNode.parentNode.setAttribute('sp_main_menu_icon', 'on');
                ele_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                ele_g = document.createElementNS('http://www.w3.org/2000/svg', "g");
                ele_path = document.createElementNS('http://www.w3.org/2000/svg', "path");
        
                ele_svg.setAttribute("viewBox", "0 0 24 24");
                ele_svg.setAttribute("class", "sp_main_menu_icon_settings");
                ele_path.setAttribute("d", "M9.5 22.375c1.583.833 3.083 1.25 4.5 1.25 1.417 0 2.896-.417 4.438-1.25 1.583-.833 2.77-1.854 3.562-3.063-.042-1.166-.98-2.145-2.813-2.937-1.833-.792-3.562-1.188-5.187-1.188-1.625 0-3.354.396-5.188 1.188-1.833.75-2.77 1.73-2.812 2.938.792 1.208 1.958 2.229 3.5 3.062zm7.313-16.5c-.792-.792-1.73-1.188-2.813-1.188-1.083 0-2.02.396-2.813 1.188C10.396 6.667 10 7.605 10 8.688c0 1.083.396 2.02 1.188 2.812.791.792 1.729 1.188 2.812 1.188 1.083 0 2.02-.396 2.813-1.188C17.604 10.708 18 9.77 18 8.687c0-1.083-.396-2.02-1.188-2.812zm-12.25-1.25C7.188 2 10.332.687 14 .687S20.792 2 23.375 4.626C26 7.208 27.313 10.333 27.313 14S26 20.813 23.375 23.438c-2.583 2.583-5.708 3.875-9.375 3.875s-6.813-1.292-9.438-3.875C1.98 20.813.688 17.666.688 14c0-3.667 1.292-6.792 3.875-9.375z");
                ele_g.appendChild(ele_path);
                ele_svg.appendChild(ele_g);
                item.appendChild(ele_svg);
                console.log(item)
            }
        })
        // console.log(3)
    }

    target_node = document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/superset/welcome/"] > svg') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/superset/welcome/"] > svg');
    if (target_node === null 
        && (document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/superset/welcome/"]') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/superset/welcome/"]'))) {
        ele_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        ele_g = document.createElementNS('http://www.w3.org/2000/svg', "g");
        ele_path = document.createElementNS('http://www.w3.org/2000/svg', "path"); 

        ele_svg.setAttribute("viewBox", "0 0 24 24");
        ele_path.setAttribute("d", "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8");
        ele_g.appendChild(ele_path);
        ele_svg.appendChild(ele_g);
        if(document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/superset/welcome/"]')) {
            document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/superset/welcome/"]').appendChild(ele_svg);
        }
        if(document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/superset/welcome/"]')) {
            document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/superset/welcome/"]').appendChild(ele_svg);
        }
    }

    target_node = document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"] > svg') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"] > svg');
    if (target_node === null
        && (document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"]') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"]'))) {
        ele_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        ele_g = document.createElementNS('http://www.w3.org/2000/svg', "g");
        ele_path = document.createElementNS('http://www.w3.org/2000/svg', "path");

        ele_svg.setAttribute("viewBox", "0 0 24 24"); 

        ele_svg.setAttribute("viewBox", "0 0 24 24");
        ele_path.setAttribute("d", "M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z");
        ele_g.appendChild(ele_path);
        ele_svg.appendChild(ele_g);
        if(document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"]')) {
            document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/dashboard/list/"]').appendChild(ele_svg);
        }
        if(document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"]')) {
            document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/dashboard/list/"]').appendChild(ele_svg);
        }
    }

    target_node = document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/chart/list/"] > svg') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/chart/list/"] > svg');
    if (target_node === null 
        && (document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/chart/list/"]') || document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/chart/list/"]'))) {
        ele_svg = document.createElement('svg');

        ele_svg.setAttribute("class", "fa fa-line-chart");
        if(document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/chart/list/"]')) {
            document.querySelector('header > div > div:nth-child(1) .css-188dvs4 [href="/chart/list/"]').appendChild(ele_svg);
        }
        if(document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/chart/list/"]')) {
            document.querySelector('header > div > div:nth-child(1) .menu-188dvs4 [href="/chart/list/"]').appendChild(ele_svg);
        }
    }
    
    // Update Filter panel on dashboards
    target_node = document.querySelector('.css-kfnq8:not(.active)');
    if(target_node) {
        document.querySelector('[aria-label="expand"]').click();
        target_node.classList.add('active');
    }
}


function Update_each_1_seconds(is_dashboard_reader_user) {
    // MAIN SRC - Update_each_1_seconds


    // update translation on page if exists
    let target_node = document.querySelector('.welcome-header');
    if(target_node) {
        if(target_node.innerText === 'Home') {target_node.innerText = 'Главная'}
    }
    // Update ant placeholder defaults
    let target_nodes = document.querySelectorAll('.ant-select-selection-placeholder');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText === "Select or type a value") {item.innerText = "выбрать или ввести значение"}})
    }
    target_nodes = document.querySelectorAll('[placeholder="Type a value"]');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {item.placeholder = "Ввести значение"})
    } 
    target_nodes = document.querySelectorAll('.ant-card-meta-description, .ant-empty-description > span');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText) {item.innerText = update_innertext(text_input=item.innerText)} })
    } 
    target_nodes = document.querySelectorAll('.switch > span');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText) {item.innerText = update_innertext(text_input=item.innerText)} })
    } 
    target_nodes = document.querySelectorAll('.ant-btn.superset-button.css-1ryksrc > span, .ant-btn.superset-button.css-1xcaxb4 > span');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText) {item.innerText = update_innertext(text_input=item.innerText)} })
    } 
    target_nodes = document.querySelectorAll('#app > .css-ublptf .css-kfnq8 > .css-1a2qin2 .ant-tabs-tab-btn, \
    #app > .css-ublptf .css-kfnq8 > .css-1a2qin2 [data-test="filter-bar__create-filter"] > span:nth-child(2), \
    #app > .css-ublptf .css-kfnq8 > .css-1a2qin2 .ant-select-selection-placeholder');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText) {item.innerText = update_innertext(text_input=item.innerText)} })
    }
    target_nodes = document.querySelectorAll('.ant-modal-root #rc-tabs-1-tab-scoping, \
    .ant-modal-root .css-sdqnu6, \
    .ant-modal-root .css-mt1npg > label > span');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText) {item.innerText = update_innertext(text_input=item.innerText)} })
    }
}


function Update_once_type_1() {
    // MAIN SRC - Update_once_type_1


    GetUserProps();

    // Get user properties
    user_data = JSON.parse(document.querySelector('[data-bootstrap]').getAttribute('data-bootstrap'));
    if(user_data.user) {
        // 
        if (user_data.user.username === 'admin' && user_data.user.email === 'admin@superset.com') {
            is_dashboard_reader_user = false;
        } else {
            // Activate Dashboard_Reader user page properties if user_exists
            is_dashboard_reader_user = (!user_data.user.roles.hasOwnProperty('Dashboards_Creator') && user_data.user.roles.hasOwnProperty('Dashboards_Reader')) || false;
            // console.log(is_dashboard_reader_user)
            if (is_dashboard_reader_user) {
                if(document.getElementById('app')) {document.getElementById('app').classList.add("Dashboard_Reader")};
                if(document.getElementById('app-menu')) {document.getElementById('app-menu').classList.add("Dashboard_Reader")};
            }
        }
    } else {
        // Anonymous user
    }

    // Hide extra filters in dashboard page for Dashboard_Reader role
    if (document.querySelector('[data-test="import-button"]')) {
        document.getElementById('app').classList.add("show_extra_controls");
    } else {
        if(document.querySelector('#app > div > div .header')) {
            if(document.querySelector('#app > div > div .header').innerText === "Дашборды") {
                document.getElementById('app').classList.remove("show_extra_controls");
            }
        }
        if(document.querySelector('#app-menu > div > div .header')) {
            if(document.querySelector('#app-menu > div > div .header').innerText === "Дашборды") {
                document.getElementById('app-menu').classList.remove("show_extra_controls");
            }
        }
    }
    // Update Filter panel on dashboards
    document.querySelector('.css-kfnq8:not(.active)')

    // change .navbar-brand-text title format
    let text_format = "Brand text <br> logo"
    let tag_span = document.createElement('span');
    let target_node = document.querySelector('#app > header > div > div > .navbar-brand-text > span');
    if(target_node) {
        tag_span.innerHTML = text_format
        target_node.parentNode.appendChild(tag_span);
        target_node.parentNode.removeChild(target_node);
    }
    target_node = document.querySelector('#app-menu > header > div > div > .navbar-brand-text > span');
    if(target_node) {
        tag_span.innerHTML = text_format
        target_node.parentNode.appendChild(tag_span);
        target_node.parentNode.removeChild(target_node);
    }
    // update missle translations for Russian lang
    // let trans_tag;
    // if (document.querySelector('li > div > .css-vdqyuj, li > div > .menu-vdqyuj')) {
    //     document.querySelector('li > div > .css-vdqyuj, li > div > .menu-vdqyuj').parentNode.parentNode.addEventListener("mouseover", function() {
    //         setTimeout(() => {
    //             trans_tag = document.querySelector('[title="About"]');
    //             trans_tag ? trans_tag.innerText = "Об программе" : null
    //         }, 1000);
    //     }, {once : true});
    // }

    // Update for ROLE: Dashboard_Reader
    let target_nodes = document.querySelectorAll('[data-test="view-query-menu-item"]');
    if(target_nodes.length > 0) {
        target_nodes.forEach((item, index) => {if(item.innerText === "Скопировать запрос") {item.parentNode.parentNode.remove()}})
    }
    return 1;
};



function Update_once_type_2() {
    // MAIN SRC - Update_once_type_2

    
    GetUserProps();
    /* close event if click on body */
    function evt_close(e) {
        console.log('function evt_close', e)
        if(document.querySelector('.css-kfnq8.active > .css-1a2qin2')) {
            if (!e.target.closest('.css-kfnq8.active > .css-1a2qin2')) {
                console.log('close ... ');
                document.querySelector('[aria-label="expand"]').click();
            }
        }
    }
    setTimeout(() => { 
        let event_node = document.querySelector('body');
        if(event_node) {
            event_node.removeEventListener("click", evt_close, false);
            event_node.addEventListener('click', evt_close, false);
        }
    }, 4000)
    console.log('INIT CUSTOM SUPERSET SCRIPTS:', 'DONE')
    return 1;
};




console.log('INIT CUSTOM SUPERSET SCRIPTS:', 'START')
// setTimeout(Update_once_type_1, 2500);
// setTimeout(Update_once_type_2, 10000);
setInterval(() => {Update_each_03_seconds(is_dashboard_reader_user)}, 300);
setInterval(() => {Update_each_1_seconds(is_dashboard_reader_user)}, 1000);
let previousUrl = '';
let Update_once_type_1_available = 1;
let Update_once_type_2_available = 1;
const observer = new MutationObserver(function(mutations) {
  if (location.href !== previousUrl) {
        previousUrl = location.href;
        // console.log(`URL changed to ${location.href}`);
        if(Update_once_type_1_available === 1) {
            Update_once_type_1_available = 0;
            setTimeout(() => { Update_once_type_1_available = Update_once_type_1() }, 2500)
        }
        if(Update_once_type_2_available === 1) {
            Update_once_type_2_available = 0;
            setTimeout(() => { Update_once_type_2_available = Update_once_type_2() }, 3500)
        }
        console.log(Update_once_type_1_available, Update_once_type_2_available);
    }
});
const config = {subtree: true, childList: true};
observer.observe(document, config);
                
    
