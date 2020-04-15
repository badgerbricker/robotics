
(cl:in-package :asdf)

(defsystem "final_project-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "position_msg" :depends-on ("_package_position_msg"))
    (:file "_package_position_msg" :depends-on ("_package"))
  ))