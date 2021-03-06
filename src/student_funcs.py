from math_funcs import make_vect, get_magnitude, dot_product
import math
import utils


def get_angle(student):
    """gets the angle of the slope of the points (best we could do), appends that angle to angle list


    Args:
       student: thestudent working on
    """
    # NOTE: a bit over engineered but its sunday :)
    # turn attention_points and reference_points into vectors
    attention_points = student.attention_points
    reference_points = student.reference_points
    
    attention_vec = make_vect(attention_points[0], attention_points[1])

    reference_vec = make_vect(reference_points[0], reference_points[1])

    # get angle between those vectors
    ## get magnitude of two vectors
    attention_mag = get_magnitude(attention_vec)
    reference_mag = get_magnitude(reference_vec)

    ## dot product
    attention_reference_dot = dot_product(attention_vec, reference_vec)
    
    angle = int(math.degrees(math.acos(attention_reference_dot/(attention_mag*reference_mag))))
    # append angle
    student.attention_angle_list.append(angle)


def get_mode_angle(student):
    """gets the mode angle (students are assumed to be paying attention most of the time)

    Args:
       student: student object


    """
    angle_list = student.attention_angle_list

    binned = [5 * round(x/5) for x in angle_list]
    mode = max(set(binned), key=binned.count)
    student.mode_attention_angle = mode


def get_attention_per_frame(student):
    """gets the ratio of the attention at frame vs mode_attention_angle

    Args:
       student: student object


    """
    attention_list = student.attention_angle_list
    mode_attention_angle = student.mode_attention_angle

    attention_angle_per_frame_raw = [abs((x - mode_attention_angle)/mode_attention_angle) for x in attention_list]

    # little hackey but mapping extreme high error to 0.00001
    attention_angle_per_frame = []
    for i in attention_angle_per_frame_raw:
        if i > 1.0:
            attention_angle_per_frame.append(.000001)
        else:
            attention_angle_per_frame.append(1 - i)

    student.attention_angle_per_frame = attention_angle_per_frame


def check_for_absent(student_list):
    """checks if student is missing for 10 frames and removes them

    Args:
       student_list: list of students

    Returns:
        list of students

    """
    i = 0
    for student in student_list:
        if student.absent_from_frame >= 10:
            student_list.pop(i)
        i += 1


def check_for_duplicate(student_list):
    """checks if the student is represented more than once then, if so it removes student

    Args:
       student_list: list of student objects

    Returns:
        updated student list

    """
    bad_list = []
    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            top_left = student_list[j].face['keypoints']['left_eye']
            bottom_right = student_list[j].face['keypoints']['mouth_right']
            box = utils.extend_box(top_left, bottom_right, 10)

            if utils.point_in_box(box, student_list[i].face_points['nose']):
                if student_list[i].present_in_frame < student_list[j].present_in_frame:
                    bad_student = student_list[i]
                else:
                    bad_student = student_list[j]
                bad_list.append(bad_student)
    good_list = [i for i in student_list if i not in bad_list]
    return good_list
