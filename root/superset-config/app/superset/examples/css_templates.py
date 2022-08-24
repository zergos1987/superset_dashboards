# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import textwrap

from superset import db
from superset.models.core import CssTemplate


def load_css_templates() -> None:
    """Loads 2 css templates to demonstrate the feature"""
    print("Creating default CSS templates")

    obj = db.session.query(CssTemplate).filter_by(template_name="Flat").first()
    if not obj:
        obj = CssTemplate(template_name="Flat")
    css = textwrap.dedent(
        """\
    .navbar {
        transition: opacity 0.5s ease;
        opacity: 0.05;
    }
    .navbar:hover {
        opacity: 1;
    }
    .chart-header .header{
        font-weight: @font-weight-normal;
        font-size: 12px;
    }
    /*
    var bnbColors = [
        //rausch    hackb      kazan      babu      lima        beach     tirol
        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',
        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',
        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',
     ];
    */
    """
    )
    obj.css = css
    db.session.merge(obj)
    db.session.commit()

    obj = db.session.query(CssTemplate).filter_by(template_name="Courier Black").first()
    if not obj:
        obj = CssTemplate(template_name="Courier Black")
    css = textwrap.dedent(
        """\
    h2 {
        color: white;
        font-size: 52px;
    }
    .navbar {
        box-shadow: none;
    }
    .navbar {
        transition: opacity 0.5s ease;
        opacity: 0.05;
    }
    .navbar:hover {
        opacity: 1;
    }
    .chart-header .header{
        font-weight: @font-weight-normal;
        font-size: 12px;
    }
    .nvd3 text {
        font-size: 12px;
        font-family: inherit;
    }
    body{
        background: #000;
        font-family: Courier, Monaco, monospace;;
    }
    /*
    var bnbColors = [
        //rausch    hackb      kazan      babu      lima        beach     tirol
        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',
        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',
        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',
     ];
    */
    """
    )
    obj.css = css
    db.session.merge(obj)
    db.session.commit()


    obj = db.session.query(CssTemplate).filter_by(template_name="Dashbord_template_main").first()
    if not obj:
        obj = CssTemplate(template_name="Dashbord_template_main")
    css = textwrap.dedent(
        """\
        /* Основа дашборда ============================================================= */
        .dashboard-component-chart-holder {
          border-radius: 17px !important;
          box-shadow: 0 2px 4px 0 rgb(0 0 0 / 7%) !important;
        }
        .dashboard-markdown .dashboard-component-chart-holder {
          border-radius: 0px !important;
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar {
          width: 14px;
          height: 14px;
          background-color: #fff;  
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }

        .css-t22g9u > div:not(.dashboard--editing) .grid-column--empty:before {
          display: None;
        }
        /* Фильтры ===================================================================== */
        [data-test-viz-type="filter_box"] {
          margin-top: 5px;
          height: calc(100% - 20px) !important;
        }

        [data-test-viz-type="filter_box"] button {
          position: absolute;
          height: 20px;
          border-radius: 12px;
          bottom: -23px;
          width: 100%;
          color: #ffffff !important;
          text-shadow: 1px 1px 1px #636363 !important;
          font-size: 11px;
          background-color: #00000054 !important;
        }

        /*заголовки*/
        [data-test-viz-type="filter_box"] .editable-title > span {
          visibility: hidden;
        }

        [data-test-viz-type="filter_box"] .filter_box {
          padding: 0 !important;
        }

        [data-test-viz-type="filter_box"] .filter_box > div {
          overflow: hidden !important;
        }

        [data-test-viz-type="filter_box"] > .chart-header {
          z-index: 10;
          position: absolute;
          right: 16px;
          top: 16px;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart {
          margin-top: 3px;
        }

        [data-test-viz-type="filter_box"] .css-6bztgs {
          margin-bottom: 12px;
          padding-left: 1px;
          width: calc(100% - 50px);
          color: #777777 !important;
          font-family: sans-serif;
          letter-spacing: 0.5px;
        }

        [data-test-viz-type="filter_box"] .Select__placeholder.css-miy1le-placeholder {
          font-size: 12px;
        }

        [data-test-viz-type="filter_box"] .Select__value-container--has-value {
          font-size: 14px;
        }

        [data-test-viz-type="filter_box"] .Select__indicator.Select__clear-indicator .fa {
          font-weight: bold;
          font-family: fantasy;
          cursor: pointer;
        }

        [data-test-viz-type="filter_box"] .Select__multi-value__remove,
        [data-test-viz-type="filter_box"] .Select__indicator.Select__dropdown-indicator {
          cursor: pointer; 
        }

        [data-test-viz-type="filter_box"] .css-lwop7g {
          width: calc(100% - 30px);
        }

        [data-test-viz-type="filter_box"] .Select__indicators.css-ytu025 {
          display: flex;
          flex-direction: column;
        }

        [data-test-viz-type="filter_box"] .Select__indicators.css-ytu025 > div {
          padding: 6px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts {
          display: flex;
          flex-direction: row;
          justify-content: center;
          padding: 6px 8px 4px 8px;
          margin-top: -1px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > .anticon.css-tp6bb2 {
          padding-left: 4px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > .anticon > svg {
          width: 16px;
          height: 16px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > span:not(.anticon) {
          font-size: 11px;
        }

        [data-test-viz-type="filter_box"] .filter_box > div {
          overflow: auto !important;
        }

        /* Выравнивание box */
        [data-test-viz-type="filter_box"] > .dashboard-chart,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container {
          height: 100% !important;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div {
          display: flex;
          flex-direction: column;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div {
          height: calc(100% - 32px) !important;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container {
          overflow-y: auto;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar  {
          width: 14px;
          height: 14px;
          background-color: #fff; 
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row {
          margin-left: 0;
          margin-right: 0;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div {
          padding: 0;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div > .ControlHeader {
          padding-bottom: 10px;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div > .ControlHeader [role="button"] {
          margin-bottom: 12px;
          padding-left: 1px;
          width: calc(100% - 50px);
          color: #777777 !important;
          font-family: sans-serif;
          letter-spacing: 0.5px;
          font-weight: 700;
        }

        [data-test-viz-type="filter_box"] > div > .header-title {
          display: None;
        }
        /* Графики - таблицы =========================================================== */
        /* скроллбар*/
        .dashboard-markdown .dashboard-component-chart-holder {
          overflow-y: hidden !important;
        }

        .dashboard-markdown .dashboard-component-chart-holder:hover {
          overflow-y: auto !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb {
          overflow: hidden !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb:hover {
          overflow: auto !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar  {
          width: 14px;
          height: 14px;
          background-color: #fff; 
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar-thumb:hover,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar-thumb,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }
        /*Фильтры*/
        [data-test-viz-type] .header-controls > .filter-counts {
          display: flex;
          flex-direction: row;
          justify-content: center;
          padding: 6px 8px 3px 8px;
        }

        [data-test-viz-type] .header-controls > .filter-counts > .anticon > svg {
          width: 16px;
          height: 16px;
        }

        [data-test-viz-type] .header-controls > .filter-counts > span:not(.anticon) {
          font-size: 11px;
        }

        /* Tools - фильтры */
        .ant-dropdown.ant-dropdown-placement-bottomRight > ul,
        .ant-dropdown.ant-dropdown-placement-bottomLeft > ul {
          box-shadow: 0 0px 2px 1px #0000003b;
          border-radius: 7px;
          background-color: #fffffff5;
        }

        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-item:hover, 
        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-submenu-title:hover,
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-item:hover, 
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-submenu-title:hover{
          background-color: #e6e6e6;
        }

        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-item,
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-item{
          font-size: 12px;
        }


        /*заголовки*/
        [data-test-viz-type] .editable-title > span {
          font-size: 18px;
          font-weight: 500;
          line-height: 24px;
          transition: color .15s;
          color: #242629;
          font-family: SeroPro,Arial,sans-serif;
        }

        /* VIZ - mixed_timeseries */
        [data-test-viz-type="mixed_timeseries"] {

        }

        /* VIZ - pivot_table_v2 */
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr th {
          border-left: 1px solid #d3d4d4;
          border-top: 1px solid #d3d4d4;
          font-size: 11px;
          font-weight: bold;
          font-family: 'Roboto';
          color: #000000;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr td {
          border-left: 1px solid #d3d4d4;
          border-top: 1px solid #d3d4d4;
          font-size: 11px;
          color: #5d5d5d;
          font-family: 'Inter';
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr td:last-child, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr th:last-child:not(.pvtSubtotalLabel) {
          border-right: 1px solid #d3d4d4;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:last-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:last-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead th.pvtSubtotalLabel, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:first-child th.pvtTotalLabel, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:nth-last-child(2) th.pvtColLabel {
          border-bottom: 1px solid #d3d4d4;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child:not(:only-child) th.pvtAxisLabel~th.pvtColLabel {
          border-top: none;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child:not(:only-child) th.pvtAxisLabel~th.pvtColLabel {
          border-top: none;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="2"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="3"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="4"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="5"]:first-child {
          border-bottom: 1px solid #d3d4d4;
        }
    """
    )
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    db.session.commit()


    obj = db.session.query(CssTemplate).filter_by(template_name="Dashbord_template_main_standalone").first()
    if not obj:
        obj = CssTemplate(template_name="Dashbord_template_main_standalone")
    css = textwrap.dedent(
        """\
        /* Основа дашборда ============================================================= */
        .dashboard-component-chart-holder {
          border-radius: 17px !important;
          box-shadow: 0 2px 4px 0 rgb(0 0 0 / 7%) !important;
        }
        .dashboard-markdown .dashboard-component-chart-holder {
          border-radius: 0px !important;
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar {
          width: 14px;
          height: 14px;
          background-color: #fff;  
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        .dashboard-component-chart-holder div[style*="overflow: auto"]::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }

        .css-t22g9u > div:not(.dashboard--editing) .grid-column--empty:before {
          display: None;
        }
        /* Фильтры ===================================================================== */
        [data-test-viz-type="filter_box"] {
          margin-top: 5px;
          height: calc(100% - 20px) !important;
        }

        [data-test-viz-type="filter_box"] button {
          position: absolute;
          height: 20px;
          border-radius: 12px;
          bottom: -23px;
          width: 100%;
          color: #ffffff !important;
          text-shadow: 1px 1px 1px #636363 !important;
          font-size: 11px;
          background-color: #00000054 !important;
        }

        /*заголовки*/
        [data-test-viz-type="filter_box"] .editable-title > span {
          visibility: hidden;
        }

        [data-test-viz-type="filter_box"] .filter_box {
          padding: 0 !important;
        }

        [data-test-viz-type="filter_box"] .filter_box > div {
          overflow: hidden !important;
        }

        [data-test-viz-type="filter_box"] > .chart-header {
          z-index: 10;
          position: absolute;
          right: 16px;
          top: 16px;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart {
          margin-top: 3px;
        }

        [data-test-viz-type="filter_box"] .css-6bztgs {
          margin-bottom: 12px;
          padding-left: 1px;
          width: calc(100% - 50px);
          color: #777777 !important;
          font-family: sans-serif;
          letter-spacing: 0.5px;
        }

        [data-test-viz-type="filter_box"] .Select__placeholder.css-miy1le-placeholder {
          font-size: 12px;
        }

        [data-test-viz-type="filter_box"] .Select__value-container--has-value {
          font-size: 14px;
        }

        [data-test-viz-type="filter_box"] .Select__indicator.Select__clear-indicator .fa {
          font-weight: bold;
          font-family: fantasy;
          cursor: pointer;
        }

        [data-test-viz-type="filter_box"] .Select__multi-value__remove,
        [data-test-viz-type="filter_box"] .Select__indicator.Select__dropdown-indicator {
          cursor: pointer; 
        }

        [data-test-viz-type="filter_box"] .css-lwop7g {
          width: calc(100% - 30px);
        }

        [data-test-viz-type="filter_box"] .Select__indicators.css-ytu025 {
          display: flex;
          flex-direction: column;
        }

        [data-test-viz-type="filter_box"] .Select__indicators.css-ytu025 > div {
          padding: 6px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts {
          display: flex;
          flex-direction: row;
          justify-content: center;
          padding: 6px 8px 4px 8px;
          margin-top: -1px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > .anticon.css-tp6bb2 {
          padding-left: 4px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > .anticon > svg {
          width: 16px;
          height: 16px;
        }

        [data-test-viz-type="filter_box"] .header-controls > .filter-counts > span:not(.anticon) {
          font-size: 11px;
        }

        [data-test-viz-type="filter_box"] .filter_box > div {
          overflow: auto !important;
        }

        /* Выравнивание box */
        [data-test-viz-type="filter_box"] > .dashboard-chart,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div,
        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container {
          height: 100% !important;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div {
          display: flex;
          flex-direction: column;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div {
          height: calc(100% - 32px) !important;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container {
          overflow-y: auto;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar  {
          width: 14px;
          height: 14px;
          background-color: #fff; 
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .filter-container > div > div > div > .Select__value-container::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row {
          margin-left: 0;
          margin-right: 0;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div {
          padding: 0;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div > .ControlHeader {
          padding-bottom: 10px;
        }

        [data-test-viz-type="filter_box"] > .dashboard-chart > .chart-container > .slice_container > .filter_box > div > .row > div > .ControlHeader [role="button"] {
          margin-bottom: 12px;
          padding-left: 1px;
          width: calc(100% - 50px);
          color: #777777 !important;
          font-family: sans-serif;
          letter-spacing: 0.5px;
          font-weight: 700;
        }

        [data-test-viz-type="filter_box"] > div > .header-title {
          display: None;
        }
        /* Графики - таблицы =========================================================== */
        /* скроллбар*/
        .dashboard-markdown .dashboard-component-chart-holder {
          overflow-y: hidden !important;
        }

        .dashboard-markdown .dashboard-component-chart-holder:hover {
          overflow-y: auto !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb {
          overflow: hidden !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb:hover {
          overflow: auto !important;
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar  {
          width: 14px;
          height: 14px;
          background-color: #fff; 
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar-thumb:hover,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar-thumb:hover {
          background-color: #a4a4a4; 
        }

        [data-test-viz-type="pivot_table_v2"] .css-kd4gnb::-webkit-scrollbar-thumb,
        .dashboard-markdown .dashboard-component-chart-holder::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border: 3px solid transparent;
          border-radius: 10px;
          background-clip: padding-box;  
        }
        /*Фильтры*/
        [data-test-viz-type] .header-controls > .filter-counts {
          display: flex;
          flex-direction: row;
          justify-content: center;
          padding: 6px 8px 3px 8px;
        }

        [data-test-viz-type] .header-controls > .filter-counts > .anticon > svg {
          width: 16px;
          height: 16px;
        }

        [data-test-viz-type] .header-controls > .filter-counts > span:not(.anticon) {
          font-size: 11px;
        }

        /* Tools - фильтры */
        .ant-dropdown.ant-dropdown-placement-bottomRight > ul,
        .ant-dropdown.ant-dropdown-placement-bottomLeft > ul {
          box-shadow: 0 0px 2px 1px #0000003b;
          border-radius: 7px;
          background-color: #fffffff5;
        }

        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-item:hover, 
        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-submenu-title:hover,
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-item:hover, 
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-submenu-title:hover{
          background-color: #e6e6e6;
        }

        .ant-dropdown.ant-dropdown-placement-bottomRight .ant-dropdown-menu-item,
        .ant-dropdown.ant-dropdown-placement-bottomLeft .ant-dropdown-menu-item{
          font-size: 12px;
        }


        /*заголовки*/
        [data-test-viz-type] .editable-title > span {
          font-size: 18px;
          font-weight: 500;
          line-height: 24px;
          transition: color .15s;
          color: #242629;
          font-family: SeroPro,Arial,sans-serif;
        }

        /* VIZ - mixed_timeseries */
        [data-test-viz-type="mixed_timeseries"] {

        }

        /* VIZ - pivot_table_v2 */
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr th {
          border-left: 1px solid #d3d4d4;
          border-top: 1px solid #d3d4d4;
          font-size: 11px;
          font-weight: bold;
          font-family: 'Roboto';
          color: #000000;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr td {
          border-left: 1px solid #d3d4d4;
          border-top: 1px solid #d3d4d4;
          font-size: 11px;
          color: #5d5d5d;
          font-family: 'Inter';
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr td:last-child, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr th:last-child:not(.pvtSubtotalLabel) {
          border-right: 1px solid #d3d4d4;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:last-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:last-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead th.pvtSubtotalLabel, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:first-child th.pvtTotalLabel, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:nth-last-child(2) th.pvtColLabel {
          border-bottom: 1px solid #d3d4d4;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child:not(:only-child) th.pvtAxisLabel~th.pvtColLabel {
          border-top: none;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child td, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr:first-child th, 
        [data-test-viz-type="pivot_table_v2"] table.pvtTable thead tr:last-child:not(:only-child) th.pvtAxisLabel~th.pvtColLabel {
          border-top: none;
        }

        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="2"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="3"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="4"]:first-child,
        [data-test-viz-type="pivot_table_v2"] table.pvtTable tbody tr > th[rowspan="5"]:first-child{
          border-bottom: 1px solid #d3d4d4;
        }

        /* ----------------------------- Standalone part ----------------------------- */

        body {
          background-color: transparent;
        }

        .dashboard-component-chart-holder {
          border: 1px solid #eaeaea !important;
        }

        .css-17fd252 .grid-container {
          margin: 30px 20px;
        }
    """
    )
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
