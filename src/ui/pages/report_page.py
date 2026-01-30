"""
Investment Report Generation Page - 투자 레포트 생성 페이지

리팩토링 버전:
- 차트 렌더링 로직을 chart_helpers.py로 분리
- 중복 코드 제거 및 가독성 향상
"""

import streamlit as st
from utils.pdf_utils import create_pdf

# ============================================================
# 차트 유틸리티 로드
# ============================================================

# Plotly 차트 (Streamlit 표시용 - 벡터 기반 선명)
PLOTLY_FUNCS = {}
PLOTLY_AVAILABLE = False
try:
    from utils.plotly_charts import (
        generate_line_chart_plotly,
        generate_candlestick_chart_plotly,
        generate_volume_chart_plotly,
        generate_financial_chart_plotly,
    )

    PLOTLY_FUNCS = {
        "generate_line_chart_plotly": generate_line_chart_plotly,
        "generate_candlestick_chart_plotly": generate_candlestick_chart_plotly,
        "generate_volume_chart_plotly": generate_volume_chart_plotly,
        "generate_financial_chart_plotly": generate_financial_chart_plotly,
    }
    PLOTLY_AVAILABLE = True
except ImportError:
    pass

# Matplotlib 차트 (PDF 내보내기용)
MPL_FUNCS = {}
CHART_UTILS_AVAILABLE = False
try:
    from utils.chart_utils import (
        generate_line_chart,
        generate_candlestick_chart,
        generate_volume_chart,
        generate_financial_chart,
    )

    MPL_FUNCS = {
        "generate_line_chart": generate_line_chart,
        "generate_candlestick_chart": generate_candlestick_chart,
        "generate_volume_chart": generate_volume_chart,
        "generate_financial_chart": generate_financial_chart,
    }
    CHART_UTILS_AVAILABLE = True
except ImportError:
    pass

# 헬퍼 함수 로드
try:
    from ui.helpers.chart_helpers import (
        render_charts_plotly,
        render_charts_matplotlib,
        resolve_tickers,
        generate_report_with_spinner,
        create_download_button,
        render_chart_selection,
    )

    HELPERS_AVAILABLE = True
except ImportError:
    HELPERS_AVAILABLE = False


# ============================================================
# CSS 스타일
# ============================================================

FORM_CSS = """
<style>
/* Form 내 수평 블록 정렬 */
div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
    align-items: flex-end !important;
    gap: 0.5rem;
}
/* 버튼 컨테이너 하단 패딩 제거 */
div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div:last-child {
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}
div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div:last-child button {
    height: 42px !important;
    margin-top: 0 !important;
}
/* 입력창 높이 맞춤 */
div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] input {
    height: 42px !important;
}
</style>
"""


# ============================================================
# 차트 렌더링 (헬퍼 사용)
# ============================================================


def render_charts(tickers: list) -> list:
    """선택된 차트 렌더링 및 PDF용 이미지 수집"""

    # 헬퍼 함수 사용
    if HELPERS_AVAILABLE:
        if PLOTLY_AVAILABLE:
            return render_charts_plotly(
                tickers,
                PLOTLY_FUNCS,
                MPL_FUNCS if CHART_UTILS_AVAILABLE else None,
            )
        elif CHART_UTILS_AVAILABLE:
            return render_charts_matplotlib(tickers, MPL_FUNCS)

    # 헬퍼가 없거나 차트 라이브러리가 없는 경우 Fallback
    # (일반적으로 발생하지 않음, 헬퍼 모듈이 프로젝트에 포함됨)
    try:
        from ui.helpers.chart_helpers import render_stock_chart_fallback

        render_stock_chart_fallback(tickers)
    except ImportError:
        st.warning("차트 헬퍼 모듈을 로드할 수 없습니다.")

    return []


# ============================================================
# 메인 렌더 함수
# ============================================================


def render():
    """Render Report Generator Page"""
    st.markdown(FORM_CSS, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">📊 레포트 생성</h1>', unsafe_allow_html=True)
    st.caption("gpt-4.1-mini 기반 | 단일 기업 분석 & 비교 분석 레포트 생성")

    st.markdown("---")

    st.info(
        "💡 **단일 분석**: `AAPL` 또는 `애플` | **비교 분석**: `애플, 마이크로소프트, 알파벳` (콤마로 구분)"
    )

    # 차트 선택 UI
    if HELPERS_AVAILABLE:
        render_chart_selection()

    # 입력 폼
    with st.form("report_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])

        with col1:
            ticker = st.text_input(
                "분석할 회사 (티커 또는 한글명)",
                placeholder="AAPL 또는 애플, 테슬라, 알파벳",
                key="report_ticker_main",
                label_visibility="collapsed",
            )

        with col2:
            generate_btn = st.form_submit_button(
                "📝 레포트 생성",
                type="primary",
                use_container_width=True,
            )

    # 레포트 생성 처리
    if generate_btn and ticker:
        _handle_report_generation(ticker)


def _handle_report_generation(ticker: str):
    """레포트 생성 처리 로직"""
    try:
        from rag.report_generator import ReportGenerator
        from ui.helpers.insights_helper import resolve_to_ticker

        generator = ReportGenerator()

        # 티커 해석
        if HELPERS_AVAILABLE:
            tickers = resolve_tickers(ticker, resolve_to_ticker)
        else:
            if "," in ticker:
                raw_terms = [t.strip() for t in ticker.split(",") if t.strip()]
                tickers = [resolve_to_ticker(t) for t in raw_terms]
            else:
                tickers = [resolve_to_ticker(ticker.strip())]

        # 레포트 생성
        if HELPERS_AVAILABLE:
            report, file_prefix = generate_report_with_spinner(generator, tickers)
        else:
            if len(tickers) > 1:
                with st.spinner(f"⚖️ {', '.join(tickers)} 비교 분석 레포트 생성 중..."):
                    report = generator.generate_comparison_report(tickers)
                    file_prefix = f"comparison_{'_'.join(tickers)}"
            else:
                with st.spinner(f"📊 {tickers[0]} 분석 레포트 생성 중..."):
                    report = generator.generate_report(tickers[0])
                    file_prefix = f"{tickers[0]}_analysis_report"

        st.markdown("---")

        # 차트 렌더링
        chart_images = render_charts(tickers)

        # 레포트 표시
        st.markdown(report)

        # 다운로드 버튼
        if HELPERS_AVAILABLE:
            create_download_button(report, file_prefix, chart_images, create_pdf)
        else:
            try:
                pdf_bytes = create_pdf(report, chart_images=chart_images)
                st.download_button(
                    label="📥 레포트 다운로드 (PDF)",
                    data=pdf_bytes,
                    file_name=f"{file_prefix}.pdf",
                    mime="application/pdf",
                )
            except Exception as pdf_err:
                st.warning(f"PDF 생성 실패, Markdown으로 대체: {pdf_err}")
                st.download_button(
                    label="📥 레포트 다운로드 (MD)",
                    data=report.encode("utf-8"),
                    file_name=f"{file_prefix}.md",
                    mime="text/markdown",
                )

    except Exception as e:
        st.error(f"레포트 생성 실패: {e}")
