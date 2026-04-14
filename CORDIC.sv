

/*
    CORDIC core based arctan calculation
    FPGA requires a lot of LUTs and resources to calculate trigonometry and FP.
    Therefore, we can use CORDIC cores, which uses vector rotations to calculate trigonometric functions.

    ex) Vectoring mode is used, and the vector is rotated at a certain degree in a cycle (i.e., tan)
*/

module ArcTan_CORDIC (
    ports
);
            
endmodule