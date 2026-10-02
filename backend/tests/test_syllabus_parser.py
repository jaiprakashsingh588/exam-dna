from backend.app.services.syllabus_parser import save_syllabus


def test_save_syllabus(tmp_path):
    data = {
        "exam": "GATE",
        "year": 2027,
        "paper": "Computer Science and Information Technology",
        "paper_code": "CS",
        "subjects": [
            {
                "id": "section-1",
                "name": "Engineering Mathematics",
                "topics": ["Discrete Mathematics", "Linear Algebra"]
            }
        ]
    }

    output_file = tmp_path / "syllabus.json"
    save_syllabus(data, str(output_file))

    assert output_file.exists()
