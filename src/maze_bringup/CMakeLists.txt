cmake_minimum_required(VERSION 3.8)
project(robot_ras_ros)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Encontra apenas o básico necessário para o gerenciamento do pacote
find_package(ament_cmake REQUIRED)

# Instalação dos diretórios
install(
    DIRECTORY urdf launch worlds params rviz models
    DESTINATION share/${PROJECT_NAME}
)

install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
