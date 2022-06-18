"""Test the prototype loop extension."""
import json
from io import StringIO

from cwltool.main import main
from .util import get_data


def test_validate_loop() -> None:
    """Affirm that a loop workflow validates with --enable-ext."""
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/single-var-loop.cwl"),
    ]
    assert main(params) == 0


def test_validate_loop_fail_no_ext() -> None:
    """Affirm that a loop workflow does not validate when --enable-ext is missing."""
    params = [
        "--validate",
        get_data("tests/loop/single-var-loop.cwl"),
    ]
    assert main(params) == 1


def test_validate_loop_fail_scatter() -> None:
    """Affirm that a loop workflow does not validate if scatter and loop directives are on the same step."""
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/invalid-loop-scatter.cwl"),
    ]
    assert main(params) == 1


def test_validate_loop_fail_when() -> None:
    """Affirm that a loop workflow does not validate if when and loop directives are on the same step."""
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/invalid-loop-when.cwl"),
    ]
    assert main(params) == 1


def test_loop_single_variable() -> None:
    """Test a simple loop case with a single variable."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/single-var-loop.cwl"),
        get_data("tests/loop/single-var-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': 10}
    assert json.loads(stream.getvalue()) == expected


def test_loop_two_variables() -> None:
    """Test a loop case with two variables, which are both back-propagated between iterations."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/two-vars-loop.cwl"),
        get_data("tests/loop/two-vars-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': 10}
    assert json.loads(stream.getvalue()) == expected


def test_loop_two_variables_single_backpropagation() -> None:
    """Test a loop case with two variables, but when only one of them is back-propagated between iterations."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/two-vars-loop-2.cwl"),
        get_data("tests/loop/two-vars-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': 10}
    assert json.loads(stream.getvalue()) == expected


def test_loop_with_all_output_method() -> None:
    """Test a loop case with outputMethod set to all."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/all-output-loop.cwl"),
        get_data("tests/loop/single-var-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': [2, 3, 4, 5, 6, 7, 8, 9, 10]}
    assert json.loads(stream.getvalue()) == expected


def test_loop_value_from() -> None:
    """Test a loop case with a variable generated by a valueFrom directive."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/value-from-loop.cwl"),
        get_data("tests/loop/two-vars-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': 10}
    assert json.loads(stream.getvalue()) == expected


def test_loop_inside_scatter() -> None:
    """Test a loop subworkflow inside a scatter step."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/loop-inside-scatter.cwl"),
        get_data("tests/loop/loop-inside-scatter-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': [10, 10, 10, 10, 10]}
    assert json.loads(stream.getvalue()) == expected


def test_nested_loops() -> None:
    """Test a workflow with two nested loops."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/loop-inside-loop.cwl"),
        get_data("tests/loop/two-vars-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': [2, 3, 4]}
    assert json.loads(stream.getvalue()) == expected


def test_nested_loops_all() -> None:
    """Test a workflow with two nested loops, both with outputMethod set to all."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/loop-inside-loop-all.cwl"),
        get_data("tests/loop/two-vars-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': [[2], [2, 3], [2, 3, 4]]}
    assert json.loads(stream.getvalue()) == expected


def test_multi_source_loop_input() -> None:
    """Test a loop with two sources, which are selected through a pickValue directive."""
    stream = StringIO()
    params = [
        "--enable-ext",
        "--validate",
        get_data("tests/loop/multi-source-loop.cwl"),
        get_data("tests/loop/single-var-loop-job.yml")
    ]
    main(params, stdout=stream)
    expected = {'o1': [2, 3, 4, 5, 8, 11, 14, 17, 20]}
    assert json.loads(stream.getvalue()) == expected
