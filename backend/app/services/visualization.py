from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.data_models import DataSet, DataModel
from app.schemas.visualization import PivotAnalysisRequest, PivotAnalysisResponse, AdhocQueryRequest, AdhocQueryResponse, SpreadsheetRequest, SpreadsheetResponse
from app.core.database import SessionLocal
import openpyxl
from openpyxl.styles import Font, Alignment
import io
import base64

class VisualizationService:
    def __init__(self):
        pass

    async def pivot_analysis(self, request: PivotAnalysisRequest) -> PivotAnalysisResponse:
        db = SessionLocal()
        try:
            # 验证数据模型是否存在
            data_model = db.query(DataModel).filter(DataModel.id == request.data_model_id).first()
            if not data_model:
                raise Exception(f"数据模型不存在: {request.data_model_id}")

            # 验证维度和度量是否存在于数据模型中
            # 处理不同格式的维度和度量数据
            dimension_names = []
            for dim in data_model.dimensions:
                if isinstance(dim, dict):
                    if 'name' in dim:
                        dimension_names.append(dim['name'])
                    elif 'field' in dim:
                        dimension_names.append(dim['field'])
                    else:
                        dimension_names.append(str(dim))
                else:
                    try:
                        dimension_names.append(dim.name)
                    except AttributeError:
                        dimension_names.append(str(dim))

            measure_names = []
            for meas in data_model.measures:
                if isinstance(meas, dict):
                    if 'name' in meas:
                        measure_names.append(meas['name'])
                    elif 'field' in meas:
                        measure_names.append(meas['field'])
                    else:
                        measure_names.append(str(meas))
                else:
                    try:
                        measure_names.append(meas.name)
                    except AttributeError:
                        measure_names.append(str(meas))

            for dim in request.dimensions:
                if dim not in dimension_names:
                    raise Exception(f"维度不存在: {dim}")

            for meas in request.measures:
                if meas not in measure_names:
                    raise Exception(f"度量不存在: {meas}")

            # 模拟透视分析结果
            # 实际项目中，这里需要根据数据模型和请求参数执行实际的数据分析
            columns = request.dimensions + request.measures
            data = []

            # 生成模拟数据
            for i in range(5):
                row = {}
                for dim in request.dimensions:
                    row[dim] = f"{dim}_value_{i}"
                for meas in request.measures:
                    row[meas] = i * 100
                data.append(row)

            return PivotAnalysisResponse(
                success=True,
                data=data,
                columns=columns,
                message="透视分析成功"
            )
        finally:
            db.close()

    async def adhoc_query(self, request: AdhocQueryRequest) -> AdhocQueryResponse:
        db = SessionLocal()
        try:
            # 验证数据集是否存在
            data_set = db.query(DataSet).filter(DataSet.id == request.data_set_id).first()
            if not data_set:
                raise Exception(f"数据集不存在: {request.data_set_id}")

            # 验证字段是否存在于数据集中
            # 处理不同格式的字段数据
            field_names = []
            for field in data_set.fields:
                if isinstance(field, dict):
                    if 'name' in field:
                        field_names.append(field['name'])
                    elif 'field' in field:
                        field_names.append(field['field'])
                    else:
                        field_names.append(str(field))
                else:
                    try:
                        field_names.append(field.name)
                    except AttributeError:
                        field_names.append(str(field))

            for field in request.fields:
                if field not in field_names:
                    raise Exception(f"字段不存在: {field}")

            # 模拟即席查询结果
            # 实际项目中，这里需要根据数据集和请求参数执行实际的查询
            data = []
            total = 1000

            # 生成模拟数据
            limit = request.limit or 1000
            offset = request.offset or 0
            for i in range(offset, min(offset + limit, total)):
                row = {}
                for field in request.fields:
                    row[field] = f"{field}_value_{i}"
                data.append(row)

            return AdhocQueryResponse(
                success=True,
                data=data,
                total=total,
                message="即席查询成功"
            )
        finally:
            db.close()

    async def spreadsheet(self, request: SpreadsheetRequest) -> SpreadsheetResponse:
        db = SessionLocal()
        try:
            # 验证数据集是否存在
            data_set = db.query(DataSet).filter(DataSet.id == request.data_set_id).first()
            if not data_set:
                raise Exception(f"数据集不存在: {request.data_set_id}")

            # 获取数据集字段
            # 处理不同格式的字段数据
            field_names = []
            for field in data_set.fields:
                if isinstance(field, dict):
                    if 'name' in field:
                        field_names.append(field['name'])
                    elif 'field' in field:
                        field_names.append(field['field'])
                    else:
                        field_names.append(str(field))
                else:
                    try:
                        field_names.append(field.name)
                    except AttributeError:
                        field_names.append(str(field))

            # 创建Excel工作簿
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = "数据"

            # 添加表头
            for col_idx, field_name in enumerate(field_names, 1):
                cell = worksheet.cell(row=1, column=col_idx, value=field_name)
                # 设置表头样式
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')
                # 调整列宽
                worksheet.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = max(15, len(str(field_name)) + 2)

            # 生成模拟数据（实际项目中应从数据库查询）
            # 这里根据字段名生成模拟数据
            for row_idx in range(2, 11):  # 生成9行数据
                for col_idx, field_name in enumerate(field_names, 1):
                    # 根据字段名生成不同类型的模拟数据
                    if any(keyword in str(field_name).lower() for keyword in ['id', '编号']):
                        value = row_idx - 1
                    elif any(keyword in str(field_name).lower() for keyword in ['name', '名称']):
                        value = f"{field_name}_{row_idx - 1}"
                    elif any(keyword in str(field_name).lower() for keyword in ['date', '时间', '日期']):
                        value = f"2024-02-{row_idx:02d}"
                    elif any(keyword in str(field_name).lower() for keyword in ['amount', '金额', '销售', '利润']):
                        value = (row_idx - 1) * 1000.50
                    elif any(keyword in str(field_name).lower() for keyword in ['count', '数量']):
                        value = (row_idx - 1) * 10
                    else:
                        value = f"值_{row_idx - 1}"
                    
                    worksheet.cell(row=row_idx, column=col_idx, value=value)

            # 添加汇总行
            summary_row = len(field_names) + 2
            worksheet.cell(row=summary_row, column=1, value="总计")
            worksheet.cell(row=summary_row, column=1).font = Font(bold=True)
            
            # 对数值列添加汇总
            for col_idx, field_name in enumerate(field_names[1:], 2):
                if any(keyword in str(field_name).lower() for keyword in ['amount', '金额', '销售', '利润', 'count', '数量']):
                    cell = worksheet.cell(row=summary_row, column=col_idx)
                    # 添加SUM公式
                    cell.value = f"=SUM({openpyxl.utils.get_column_letter(col_idx)}2:{openpyxl.utils.get_column_letter(col_idx)}{len(field_names) + 1})"
                    cell.font = Font(bold=True)

            # 将工作簿转换为字节流
            output = io.BytesIO()
            workbook.save(output)
            output.seek(0)
            
            # 转换为base64字符串
            workbook_base64 = base64.b64encode(output.read()).decode('utf-8')

            # 生成前端需要的cells格式数据
            cells = {}
            # 添加表头
            for col_idx, field_name in enumerate(field_names, 1):
                cell_key = f"{openpyxl.utils.get_column_letter(col_idx)}1"
                cells[cell_key] = field_name
            # 添加数据行
            for row_idx in range(2, 11):  # 对应之前生成的9行数据
                for col_idx, field_name in enumerate(field_names, 1):
                    cell_key = f"{openpyxl.utils.get_column_letter(col_idx)}{row_idx}"
                    # 生成与之前相同的模拟数据
                    if any(keyword in str(field_name).lower() for keyword in ['id', '编号']):
                        value = row_idx - 1
                    elif any(keyword in str(field_name).lower() for keyword in ['name', '名称']):
                        value = f"{field_name}_{row_idx - 1}"
                    elif any(keyword in str(field_name).lower() for keyword in ['date', '时间', '日期']):
                        value = f"2024-02-{row_idx:02d}"
                    elif any(keyword in str(field_name).lower() for keyword in ['amount', '金额', '销售', '利润']):
                        value = (row_idx - 1) * 1000.50
                    elif any(keyword in str(field_name).lower() for keyword in ['count', '数量']):
                        value = (row_idx - 1) * 10
                    else:
                        value = f"值_{row_idx - 1}"
                    cells[cell_key] = value
            # 添加汇总行
            summary_row = 11
            cells[f"A{summary_row}"] = "总计"
            for col_idx, field_name in enumerate(field_names[1:], 2):
                if any(keyword in str(field_name).lower() for keyword in ['amount', '金额', '销售', '利润', 'count', '数量']):
                    cell_key = f"{openpyxl.utils.get_column_letter(col_idx)}{summary_row}"
                    # 计算汇总值
                    total = sum((i - 1) * 1000.50 if 'amount' in str(field_name).lower() or '金额' in str(field_name) else (i - 1) * 10 for i in range(2, 11))
                    cells[cell_key] = total

            # 准备响应数据
            data = {
                "template_id": request.template_id,
                "parameters": request.parameters,
                "data_set_id": request.data_set_id,
                "sheet_name": "数据",
                "field_count": len(field_names),
                "row_count": 10,  # 包含表头
                "workbook_base64": workbook_base64,
                "file_name": f"数据集_{request.data_set_id}_导出.xlsx",
                "cells": cells  # 添加前端需要的cells格式数据
            }

            return SpreadsheetResponse(
                success=True,
                data=data,
                message="电子表格生成成功"
            )
        finally:
            db.close()

visualization_service = VisualizationService()
