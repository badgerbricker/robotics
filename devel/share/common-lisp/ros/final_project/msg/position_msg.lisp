; Auto-generated. Do not edit!


(cl:in-package final_project-msg)


;//! \htmlinclude position_msg.msg.html

(cl:defclass <position_msg> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:fixnum
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:fixnum
    :initform 0)
   (z
    :reader z
    :initarg :z
    :type cl:fixnum
    :initform 0))
)

(cl:defclass position_msg (<position_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <position_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'position_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name final_project-msg:<position_msg> is deprecated: use final_project-msg:position_msg instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <position_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader final_project-msg:x-val is deprecated.  Use final_project-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <position_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader final_project-msg:y-val is deprecated.  Use final_project-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'z-val :lambda-list '(m))
(cl:defmethod z-val ((m <position_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader final_project-msg:z-val is deprecated.  Use final_project-msg:z instead.")
  (z m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <position_msg>) ostream)
  "Serializes a message object of type '<position_msg>"
  (cl:let* ((signed (cl:slot-value msg 'x)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'z)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <position_msg>) istream)
  "Deserializes a message object of type '<position_msg>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'z) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<position_msg>)))
  "Returns string type for a message object of type '<position_msg>"
  "final_project/position_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'position_msg)))
  "Returns string type for a message object of type 'position_msg"
  "final_project/position_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<position_msg>)))
  "Returns md5sum for a message object of type '<position_msg>"
  "85729383565f7e059d4a213b3db1317b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'position_msg)))
  "Returns md5sum for a message object of type 'position_msg"
  "85729383565f7e059d4a213b3db1317b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<position_msg>)))
  "Returns full string definition for message of type '<position_msg>"
  (cl:format cl:nil "int16 x~%int16 y~%int16 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'position_msg)))
  "Returns full string definition for message of type 'position_msg"
  (cl:format cl:nil "int16 x~%int16 y~%int16 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <position_msg>))
  (cl:+ 0
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <position_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'position_msg
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':z (z msg))
))
