"""
데이터 시각화 모듈
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any


def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str = "", 
                     color: Optional[str] = None, horizontal: bool = False) -> go.Figure:
    """
    막대 그래프 생성
    
    Args:
        df: 데이터프레임
        x: X축 컬럼명
        y: Y축 컬럼명
        title: 차트 제목
        color: 색상 구분 컬럼
        horizontal: 가로 막대 그래프 여부
        
    Returns:
        Plotly Figure 객체
    """
    if horizontal:
        fig = px.bar(df, x=y, y=x, title=title, color=color, orientation='h')
    else:
        fig = px.bar(df, x=x, y=y, title=title, color=color)
    
    fig.update_layout(
        template="plotly_white",
        hovermode='x unified',
        showlegend=True if color else False
    )
    
    return fig


def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str = "",
                      color: Optional[str] = None) -> go.Figure:
    """
    선 그래프 생성
    
    Args:
        df: 데이터프레임
        x: X축 컬럼명
        y: Y축 컬럼명
        title: 차트 제목
        color: 색상 구분 컬럼
        
    Returns:
        Plotly Figure 객체
    """
    fig = px.line(df, x=x, y=y, title=title, color=color, markers=True)
    
    fig.update_layout(
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig


def create_scatter_plot(df: pd.DataFrame, x: str, y: str, title: str = "",
                       color: Optional[str] = None, size: Optional[str] = None) -> go.Figure:
    """
    산점도 생성
    
    Args:
        df: 데이터프레임
        x: X축 컬럼명
        y: Y축 컬럼명
        title: 차트 제목
        color: 색상 구분 컬럼
        size: 크기 구분 컬럼
        
    Returns:
        Plotly Figure 객체
    """
    fig = px.scatter(df, x=x, y=y, title=title, color=color, size=size,
                     hover_data=df.columns)
    
    fig.update_layout(
        template="plotly_white",
        hovermode='closest'
    )
    
    return fig


def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str = "") -> go.Figure:
    """
    파이 차트 생성
    
    Args:
        df: 데이터프레임
        names: 레이블 컬럼명
        values: 값 컬럼명
        title: 차트 제목
        
    Returns:
        Plotly Figure 객체
    """
    fig = px.pie(df, names=names, values=values, title=title)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template="plotly_white")
    
    return fig


def create_histogram(df: pd.DataFrame, x: str, title: str = "",
                    nbins: int = 30, color: Optional[str] = None) -> go.Figure:
    """
    히스토그램 생성
    
    Args:
        df: 데이터프레임
        x: X축 컬럼명
        title: 차트 제목
        nbins: 구간 수
        color: 색상 구분 컬럼
        
    Returns:
        Plotly Figure 객체
    """
    fig = px.histogram(df, x=x, title=title, nbins=nbins, color=color)
    
    fig.update_layout(
        template="plotly_white",
        bargap=0.1
    )
    
    return fig


def create_box_plot(df: pd.DataFrame, x: Optional[str], y: str, title: str = "",
                   color: Optional[str] = None) -> go.Figure:
    """
    박스 플롯 생성
    
    Args:
        df: 데이터프레임
        x: X축 컬럼명 (카테고리)
        y: Y축 컬럼명 (숫자)
        title: 차트 제목
        color: 색상 구분 컬럼
        
    Returns:
        Plotly Figure 객체
    """
    fig = px.box(df, x=x, y=y, title=title, color=color)
    
    fig.update_layout(template="plotly_white")
    
    return fig


def create_heatmap(df: pd.DataFrame, title: str = "") -> go.Figure:
    """
    상관관계 히트맵 생성
    
    Args:
        df: 데이터프레임 (숫자형 컬럼만)
        title: 차트 제목
        
    Returns:
        Plotly Figure 객체
    """
    # 숫자형 컬럼만 선택
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    # 상관관계 계산
    corr = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="상관계수")
    ))
    
    fig.update_layout(
        title=title or "상관관계 히트맵",
        template="plotly_white",
        width=700,
        height=700
    )
    
    return fig


def auto_visualize(df: pd.DataFrame, question: str = "") -> go.Figure:
    """
    데이터프레임을 자동으로 분석하여 적절한 시각화 생성
    
    Args:
        df: 데이터프레임
        question: 원래 질문 (힌트로 사용)
        
    Returns:
        Plotly Figure 객체
    """
    if len(df) == 0:
        # 빈 차트
        fig = go.Figure()
        fig.add_annotation(
            text="표시할 데이터가 없습니다",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    # 컬럼 타입 분석
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # 시각화 선택 로직
    if len(numeric_cols) >= 2 and len(df) > 1:
        # 산점도
        return create_scatter_plot(df, numeric_cols[0], numeric_cols[1],
                                  title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
    
    elif len(text_cols) >= 1 and len(numeric_cols) >= 1:
        # 막대 그래프
        # 데이터가 많으면 상위 20개만
        if len(df) > 20:
            df_plot = df.nlargest(20, numeric_cols[0])
        else:
            df_plot = df
        
        return create_bar_chart(df_plot, text_cols[0], numeric_cols[0],
                               title=f"{text_cols[0]}별 {numeric_cols[0]}")
    
    elif len(numeric_cols) == 1:
        # 히스토그램
        return create_histogram(df, numeric_cols[0],
                               title=f"{numeric_cols[0]} 분포")
    
    else:
        # 기본: 테이블 형태로 표시 (빈 차트 + 메시지)
        fig = go.Figure()
        fig.add_annotation(
            text="테이블 형태로 데이터를 확인하세요",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig


def create_multi_chart(df: pd.DataFrame, chart_configs: list) -> list:
    """
    여러 차트를 한 번에 생성
    
    Args:
        df: 데이터프레임
        chart_configs: 차트 설정 리스트
            예: [{"type": "bar", "x": "genre", "y": "count"}, ...]
            
    Returns:
        Figure 객체 리스트
    """
    figures = []
    
    for config in chart_configs:
        chart_type = config.get("type", "bar")
        
        if chart_type == "bar":
            fig = create_bar_chart(df, config["x"], config["y"], 
                                  config.get("title", ""))
        elif chart_type == "line":
            fig = create_line_chart(df, config["x"], config["y"],
                                   config.get("title", ""))
        elif chart_type == "scatter":
            fig = create_scatter_plot(df, config["x"], config["y"],
                                     config.get("title", ""))
        elif chart_type == "pie":
            fig = create_pie_chart(df, config["names"], config["values"],
                                  config.get("title", ""))
        elif chart_type == "histogram":
            fig = create_histogram(df, config["x"], config.get("title", ""))
        elif chart_type == "box":
            fig = create_box_plot(df, config.get("x"), config["y"],
                                 config.get("title", ""))
        else:
            continue
        
        figures.append(fig)
    
    return figures

