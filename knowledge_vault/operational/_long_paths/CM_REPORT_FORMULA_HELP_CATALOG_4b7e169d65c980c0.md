# CM Report Formula Help Catalog

**Source:** Chromeleon 7 Help, `FormulaFunctions` and `ReportVariables_CSH`  
**Help root used:** `C:\ProgramData\CMBX Data Explorer Workspace\KB\Method Script Generator\TCC\report_template_cmbx\CM7Help_EN`  
**Coverage:** 128 FormulaOne function topics; 994 report-variable topics.

## Purpose and Boundary

This catalog is an official-Help index for web authoring. It is not evidence that every topic is available in every instrument configuration or that CMBX Data Explorer evaluates every formula locally. Use an observed carrier formula and configuration evidence before declaring a generated CM report formula runnable.

FormulaOne functions are workbook-layer functions. CM report variables are direct `ReportFormulaObject` / report-table sources; do not mix the two engines.

## FormulaOne Function Topics

These function names come from the FormulaOne Help collection. The V0.2 report compiler can persist a formula in an existing cell, but only functions marked verified by a control matrix have end-to-end evidence in this project.

| Function | Help summary | Help topic |
|---|---|---|
| `ABS` | ABS returns the absolute value of a number. | `FormulaFunctions/IDH_ABS.htm` |
| `ACOS` | ACOS returns the arc cosine of a number. | `FormulaFunctions/IDH_ACOS.htm` |
| `ACOSH` | ACOSH returns the inverse hyperbolic cosine of a number. | `FormulaFunctions/IDH_ACOSH.htm` |
| `ADDRESS` | ADDRESS creates a cell address as text. | `FormulaFunctions/IDH_ADDRESS.htm` |
| `AND` | AND returns True if all arguments are true; AND returns False if at least one argument is false. | `FormulaFunctions/IDH_AND.htm` |
| `ASC` | ASC returns a copy of text in which the double-byte characters (if any) have been converted to single-byte. Any double-byte characters that do not have single-byte equivalents are left in their original form. | `FormulaFunctions/IDH_ASC.htm` |
| `ASIN` | ASIN returns the arcsine of a number. | `FormulaFunctions/IDH_ASIN.htm` |
| `ASINH` | ASINH returns the inverse hyperbolic sine of a number. | `FormulaFunctions/IDH_ASINH.htm` |
| `ATAN` | ATAN returns the arctangent of a number. | `FormulaFunctions/IDH_ATAN.htm` |
| `ATAN2` | ATAN2 returns the arctangent of the specified coordinates. | `FormulaFunctions/IDH_ATAN2.htm` |
| `ATANH` | ATANH returns the inverse hyperbolic tangent of a number. | `FormulaFunctions/IDH_ATANH.htm` |
| `AVERAGE` | AVERAGE returns the average of the supplied numbers. The result of AVERAGE is also known as the arithmetic mean. | `FormulaFunctions/IDH_AVERAGE.htm` |
| `CEILING` | CEILING rounds a number up to the nearest multiple of a specified value. | `FormulaFunctions/IDH_CEILING.htm` |
| `CHAR` | CHAR returns a character that corresponds to the supplied ASCII code. | `FormulaFunctions/IDH_CHAR.htm` |
| `CHOOSE` | CHOOSE returns a value from a list of numbers based on the index number supplied. | `FormulaFunctions/IDH_CHOOSE.htm` |
| `CLEAN` | CLEAN removes all nonprintable characters from the supplied text. | `FormulaFunctions/IDH_CLEAN.htm` |
| `CODE` | CODE returns a numeric code representing the first character of the supplied string. | `FormulaFunctions/IDH_CODE.htm` |
| `COLUMN` | COLUMN returns the column number of the supplied reference. | `FormulaFunctions/IDH_COLUMN.htm` |
| `COLUMNS` | COLUMNS returns the number of columns in a range reference. | `FormulaFunctions/IDH_COLUMNS.htm` |
| `CONCATENATE` | CONCATENATE joins several text strings into one string. | `FormulaFunctions/IDH_CONCATENATE.htm` |
| `CORREL` | CORREL returns the correlation coefficient of the array1 and array2 cell ranges. Use the correlation coefficient to determine the relationship between two properties. | `FormulaFunctions/IDH_CORREL.htm` |
| `COS` | COS returns the cosine of an angle. | `FormulaFunctions/IDH_COS.htm` |
| `COSH` | COSH returns the hyperbolic cosine of a number. | `FormulaFunctions/IDH_COSH.htm` |
| `COUNT` | COUNT returns the number of values in the supplied list. | `FormulaFunctions/IDH_COUNT.htm` |
| `COUNTA` | COUNTA returns the number of nonblank values in the supplied list. | `FormulaFunctions/IDH_COUNTA.htm` |
| `COUNTIF` | COUNTIF returns the number of cells within a range, which meet the given criteria. | `FormulaFunctions/IDH_COUNTIF.htm` |
| `DATE` | DATE returns the serial number of the supplied date. | `FormulaFunctions/IDH_DATE.htm` |
| `DATEVALUE` | DATEVALUE returns the serial number of a date supplied as a text string. | `FormulaFunctions/IDH_DATEVALUE.htm` |
| `DAY` | DAY returns the day of the month that corresponds to the date represented by the supplied number. | `FormulaFunctions/IDH_DAY.htm` |
| `DAYS360` | DAYS360 returns the number of days between two dates based on a 360-day year (twelve 30-day months). Use this function to help compute payments if your accounting system is based on twelve 30-day months. | `FormulaFunctions/IDH_DAYS360.htm` |
| `DBCS` | DBCS returns a copy of text in which the single-byte characters (if any) have been converted to double-byte characters. Any single-byte characters that do not have double-byte equivalents are left in their original (single-byte) form. | `FormulaFunctions/IDH_DBCS.htm` |
| `ERROR.TYPE` | ERROR.TYPE returns a number corresponding to an error. | `FormulaFunctions/IDH_ERROR_TYPE.htm` |
| `EVEN` | With positive values the specified number is rounded up to the nearest even integer. Negative numbers are rounded down. | `FormulaFunctions/IDH_EVEN.htm` |
| `EXACT` | EXACT compares two expressions for identical, case-sensitive matches. True is returned if the expressions are identical; False is returned if they are not. | `FormulaFunctions/IDH_EXACT.htm` |
| `EXP` | EXP returns e raised to the specified power. The constant e is 2.71828182845904 (the base of the natural logarithm). | `FormulaFunctions/IDH_EXP.htm` |
| `FACT` | FACT returns the factorial of a specified number. | `FormulaFunctions/IDH_FACT.htm` |
| `FALSE` | F ALSE returns the logical value False. This function always requires the trailing parentheses. | `FormulaFunctions/IDH_FALSE.htm` |
| `FIND` | FIND searches for a string of text within another text string and returns the character position at which the search string first occurs. | `FormulaFunctions/IDH_FIND.htm` |
| `FINDB` | FINDB searches for a string of text within another text string and returns the byte position at which the search string first occurs. FINDB is intended for use with languages that use the double-byte character set (DBCS). | `FormulaFunctions/IDH_FINDB.htm` |
| `FIXED` | FIXED rounds a number to the supplied precision, formats the number in decimal format, and returns the result as text. | `FormulaFunctions/IDH_FIXED_1.htm` |
| `FLOOR` | FLOOR rounds a number down to the nearest multiple of a specified precision. | `FormulaFunctions/IDH_FLOOR.htm` |
| `Formula Functions` | Formulas are equations that perform calculations on values in your worksheet. A formula always starts with an equal sign (=). You may know these functions from Microsoft Excel. They can be grouped in the following categories: | `FormulaFunctions/IDH_FORMULA_OVERVIEW.htm` |
| `HLOOKUP` | HLOOKUP searches the top row of a table for a value and returns the contents of a cell in that table that corresponds to the location of the search value. | `FormulaFunctions/IDH_HLOOKUP.htm` |
| `HOUR` | HOUR returns the hour component of the specified time in 24-hour format. | `FormulaFunctions/IDH_HOUR.htm` |
| `IF` | IF tests the condition and returns the specified value. | `FormulaFunctions/IDH_IF.htm` |
| `INDEX` | INDEX returns the contents of a cell from a specified range. | `FormulaFunctions/IDH_INDEX.htm` |
| `INDIRECT` | INDIRECT returns the contents of the cell referenced by the specified cell. | `FormulaFunctions/IDH_INDIRECT.htm` |
| `INT` | INT rounds the supplied number down to the nearest integer. | `FormulaFunctions/IDH_INT.htm` |
| `INTERCEPT` | INTERCEPT calculates the value at which the linear regression line based on known_y's and known_x's intersects the y-axis. If known_y's and known_x's are empty or have a different number of data points, INTERCEPT returns the #N/A error value. | `FormulaFunctions/IDH_INTERCEPT.htm` |
| `ISBLANK` | ISBLANK determines if the specified cell is blank. | `FormulaFunctions/IDH_ISBLANK.htm` |
| `ISERR` | ISERR determines if the specified expression returns an error value. | `FormulaFunctions/IDH_ISERR.htm` |
| `ISERROR` | ISERROR determines if the specified expression returns an error value. | `FormulaFunctions/IDH_ISERROR.htm` |
| `ISLOGICAL` | ISLOGICAL determines if the specified expression returns a logical value. | `FormulaFunctions/IDH_ISLOGICAL.htm` |
| `ISNA` | ISNA determines if the specified expression returns the "value not available" error. | `FormulaFunctions/IDH_ISNA.htm` |
| `ISNONTEXT` | ISNONTEXT determines if the specified expression is not text. | `FormulaFunctions/IDH_ISNONTEXT.htm` |
| `ISNUMBER` | ISNUMBER determines if the specified expression is a number. | `FormulaFunctions/IDH_ISNUMBER.htm` |
| `ISREF` | ISREF determines if the specified expression is a range reference. | `FormulaFunctions/IDH_ISREF.htm` |
| `ISTEXT` | ISTEXT determines if the specified expression is text. | `FormulaFunctions/IDH_ISTEXT.htm` |
| `LEFT` | LEFT returns the leftmost characters from the specified text string. | `FormulaFunctions/IDH_LEFT.htm` |
| `LEFTB` | LEFTB returns the leftmost byte from the specified text string. | `FormulaFunctions/IDH_LEFTB.htm` |
| `LEN` | LEN returns the number of characters in the supplied text string. | `FormulaFunctions/IDH_LEN.htm` |
| `LENB` | LENB returns the number of bytes in the supplied text string. | `FormulaFunctions/IDH_LENB.htm` |
| `LN` | LN returns the natural logarithm (based on the constant e) of a number. | `FormulaFunctions/IDH_LN.htm` |
| `LOG` | LOG returns the logarithm of a number to the specified base. | `FormulaFunctions/IDH_LOG.htm` |
| `LOG10` | LGO10 returns the base-10 logarithm of a number. | `FormulaFunctions/IDH_LOG10.htm` |
| `LOOKUP` | LOOKUP searches for a value in one range and returns the contents of the corresponding position in a second range. Use the function when you have a large list of values to look up or when the values may change over time. | `FormulaFunctions/IDH_LOOKUP.htm` |
| `LOWER` | LOWER changes the characters in the specified string to lowercase characters. Numeric characters in the string are not changed. | `FormulaFunctions/IDH_LOWER.htm` |
| `MATCH` | A specified value is compared against values in a range. The position of the matching value in the search range is returned. | `FormulaFunctions/IDH_MATCH.htm` |
| `MAX` | MAX returns the largest value in the specified list of numbers. | `FormulaFunctions/IDH_MAX.htm` |
| `MID` | MID returns the specified number of characters from a text string, beginning with the specified starting position. | `FormulaFunctions/IDH_MID.htm` |
| `MIDB` | MIDB returns the specified number of bytes from a text string, beginning with the specified starting position. | `FormulaFunctions/IDH_MIDB.htm` |
| `MIN` | MIN returns the smallest value in the specified list of numbers. | `FormulaFunctions/IDH_MIN.htm` |
| `MINUTE` | MINUTE returns the minute that corresponds to the supplied date. | `FormulaFunctions/IDH_MINUTE.htm` |
| `MOD` | MOD returns the remainder after dividing a number by a specified divisor. | `FormulaFunctions/IDH_MOD.htm` |
| `MONTH` | MONTH returns the month that corresponds to the supplied date. | `FormulaFunctions/IDH_MONTH.htm` |
| `N` | N tests the supplied value and returns the value if it is a number. | `FormulaFunctions/IDH_N.htm` |
| `NA` | NA returns the error value #N/A, which represents not available. | `FormulaFunctions/IDH_NA.htm` |
| `NOT` | NOT returns a logical value that is the opposite of its value. | `FormulaFunctions/IDH_NOT.htm` |
| `NOW` | NOW returns the current date and time as a serial number. | `FormulaFunctions/IDH_NOW.htm` |
| `ODD` | ODD rounds the specified number up to the nearest odd integer. | `FormulaFunctions/IDH_ODD.htm` |
| `OFFSET` | OFFSET returns the contents of a range that is offset from a starting point in the spreadsheet. | `FormulaFunctions/IDH_OFFSET.htm` |
| `OR` | OR returns True if at least one of a series of logical arguments is true. | `FormulaFunctions/IDH_OR.htm` |
| `PI` | PI returns the value of pi (p), which is approximately 3.14159265358979 when calculated to 15 significant digits. | `FormulaFunctions/IDH_PI.htm` |
| `PRODUCT` | PRODUCT multiplies a list of numbers and returns the result. | `FormulaFunctions/IDH_PRODUCT.htm` |
| `PROPER` | PROPER returns the specified string in proper-case format. | `FormulaFunctions/IDH_PROPER.htm` |
| `RAND` | RAND returns a number selected randomly from a uniform distribution greater than or equal to 0 and less than 1. | `FormulaFunctions/IDH_RAND.htm` |
| `REPLACE` | REPLACE replaces part of a text string with another text string. | `FormulaFunctions/IDH_REPLACE.htm` |
| `REPLACEB` | REPLACEB replaces part of a text string with another text string. | `FormulaFunctions/IDH_REPLACEB.htm` |
| `REPT` | REPT repeats a text string the specified number of times. | `FormulaFunctions/IDH_REPT.htm` |
| `RIGHT` | RIGHT returns the rightmost characters from the given text string. | `FormulaFunctions/IDH_RIGHT.htm` |
| `RIGHTB` | RIGHTB returns the rightmost bytes from the given text string. | `FormulaFunctions/IDH_RIGHTB.htm` |
| `ROUND` | ROUND rounds the given number to the supplied number of decimal places. | `FormulaFunctions/IDH_ROUND.htm` |
| `ROUNDDOWN` | ROUNDDOWN rounds a number down. | `FormulaFunctions/IDH_ROUNDDOWN.htm` |
| `ROUNDUP` | ROUNDUP rounds the given number up to the supplied number of decimal places. | `FormulaFunctions/IDH_ROUNDUP.htm` |
| `ROW` | ROW returns the row number of the supplied reference. | `FormulaFunctions/IDH_ROW.htm` |
| `ROWS` | ROW returns the number of rows in a range reference. | `FormulaFunctions/IDH_ROWS.htm` |
| `SEARCH` | SEARCH locates the position of the first character of a specified text string within another text string. | `FormulaFunctions/IDH_SEARCH.htm` |
| `SEARCHB` | SERACHB locates the position of the first byte of a specified text string within another text string. | `FormulaFunctions/IDH_SEARCHB.htm` |
| `SECOND` | SECOND returns the second that corresponds to the supplied date. | `FormulaFunctions/IDH_SECOND.htm` |
| `SIGN` | SIGN determines the sign of the specified number. | `FormulaFunctions/IDH_SIGN.htm` |
| `SIN` | SIN returns the sine of the supplied angle. | `FormulaFunctions/IDH_SIN.htm` |
| `SINH` | SINH returns the hyperbolic sine of the specified number. | `FormulaFunctions/IDH_SINH.htm` |
| `SLOPE` | SLOPE returns the slope of the linear regression line through data points in known_y's and known_x's. The slope is the vertical distance divided by the horizontal distance between any two points on the line, which is the rate of change along the regression line. | `FormulaFunctions/IDH_SLOPE.htm` |
| `SQRT` | SQRT returns the square root of the specified number. | `FormulaFunctions/IDH_SQRT.htm` |
| `STDEV` | STDEV estimates the standard deviation based on a random sample. The standard deviation is a measure for the deviation from the average value (the mean). | `FormulaFunctions/IDH_STDEV.htm` |
| `STDEVP` | STDEVP returns the standard deviation based on the entire population of values. The standard deviation is a measure for the deviation from the average value (the mean). | `FormulaFunctions/IDH_STDEVP.htm` |
| `SUBSTITUTE` | SUBSTITUTE replaces a specified part of a text string with another text string. | `FormulaFunctions/IDH_SUBSTITUTE.htm` |
| `SUM` | SUM returns the sum of the supplied numbers. | `FormulaFunctions/IDH_SUM.htm` |
| `SUMIF` | SUMIF returns the sum of the specified cells based on the given criteria. | `FormulaFunctions/IDH_SUMIF.htm` |
| `SUMSQ` | SUMSQ squares each of the supplied numbers and returns the sum of the squares. | `FormulaFunctions/IDH_SUMSQ.htm` |
| `T` | T tests the supplied value and returns the value if it is text. | `FormulaFunctions/IDH_T.htm` |
| `TAN` | TAN returns the tangent of the specified angle. | `FormulaFunctions/IDH_TAN.htm` |
| `TANH` | TANH returns the hyperbolic tangent of a number. | `FormulaFunctions/IDH_TANH.htm` |
| `TEXT` | TEXT returns the given number as text, using the specified formatting. | `FormulaFunctions/IDH_TEXT.htm` |
| `TIME` | TIME returns a serial number for the supplied time. | `FormulaFunctions/IDH_TIME.htm` |
| `TIMEVALUE` | TIMEVALUE returns a serial number for the supplied text representation of time. | `FormulaFunctions/IDH_TIMEVALUE.htm` |
| `TODAY` | TODAY returns the current date as a serial number. | `FormulaFunctions/IDH_TODAY.htm` |
| `TRIM` | TRIM removes all spaces from text except single spaces between words. | `FormulaFunctions/IDH_TRIM.htm` |
| `TRUE` | TRUE returns the logical value True. This function always requires the trailing parentheses. | `FormulaFunctions/IDH_TRUE.htm` |
| `TRUNC` | TRUNC truncates the given number to an integer. | `FormulaFunctions/IDH_TRUNC.htm` |
| `TYPE` | TYPE returns the argument type of the given expression. | `FormulaFunctions/IDH_TYPE.htm` |
| `UPPER` | UPPER changes the characters in the specified string to uppercase characters. | `FormulaFunctions/IDH_UPPER.htm` |
| `VALUE` | VALUE returns the specified text as a number. | `FormulaFunctions/IDH_VALUE.htm` |
| `VAR` | VAR returns the variance of a population based on a sample of values. | `FormulaFunctions/IDH_VAR.htm` |
| `VARP` | VARP returns the variance of a population based on an entire population of values. | `FormulaFunctions/IDH_VARP.htm` |
| `VLOOKUP` | VLOOKUP searches the first column of a table for a value and returns the contents of a cell in that table that corresponds to the location of the search value. | `FormulaFunctions/IDH_VLOOKUP.htm` |
| `WEEKDAY` | WEEKDAY returns the day of the week that corresponds to the supplied date. | `FormulaFunctions/IDH_WEEKDAY.htm` |
| `YEAR` | YEAR returns the year that corresponds to the supplied date. | `FormulaFunctions/IDH_YEAR.htm` |

## Direct CM Report Variable Topics

### Peak

**Official Help topics:** 120

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Peak Calibration Category | The Peak Calibration category includes variables that provide information about calibration values and settings. The following table lists the variables in the Peak Calibration category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_Calibration.htm` |
| Calibration Coefficient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calCoefficient.htm` |
| Calibration Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calibration_type.htm` |
| Weights | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calibration_weight.htm` |
| Calibration Mode | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calMode.htm` |
| Residual of Calibration Point X | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointDist.htm` |
| Evaluation of Calibration Function for x | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointFX.htm` |
| Calibration Point Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointStatus.htm` |
| Calibration Point Weight | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointWeight.htm` |
| Calibration Point X/Y | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointX.htm` |
| Calibration Point: X Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointXUnit.htm` |
| Calibration Point: Y Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_calPointYUnit.htm` |
| Lower/Upper Confidence Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_confUpperLimit.htm` |
| Correlation Coefficient (Linear) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_correlation_coefficient.htm` |
| Hubaux-Vos Limit of Detection | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_hvlod.htm` |
| Number of Disabled Calibration Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_nCalDisabled.htm` |
| Number of Calibration Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_nCalpoints.htm` |
| Lower/Upper Prediction Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_predUpperLimit.htm` |
| Reference Inject Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_reference_inject_volume.htm` |
| Relative Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rel_standard_deviation.htm` |
| Relative Standard Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rel_standard_error.htm` |
| RF Value (Amount/Area) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rf_value.htm` |
| Coefficient of Determination | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rQuadrat.htm` |
| DOF-Adjusted Coefficient of Determination | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_rQuadratAdj.htm` |
| Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_standard_deviation.htm` |
| Variance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_variance.htm` |
| Variance Coefficient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Calibration_variance_coefficient.htm` |
| Peak Purity and Identification Category | The Peak Purity and Identification category includes variables that provide information about the comparison of peak spectra with reference spectra. These variables will work only if a 3D field is available for the current injection. The following table lists the available variables in the Peak Purity and Identification category. Click a variable name to rea | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification.htm` |
| Amount Difference | Peak Purity and Identification Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_amountDifference.htm` |
| Peak Apex Alignment Within Charge State | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithinChargeState.htm` |
| Peak Apex Alignment Within Charge State And Isotope | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithinChargeStateAndIstope.htm` |
| Peak Apex Alignment Within Isotope | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_apexStdDevWithInIsotope.htm` |
| Composite Score | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_compScore.htm` |
| Confirmation Chromatogram | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationChm.htm` |
| Confirmation Peak | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationPeak.htm` |
| Peak Confirmation Ratio | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationRatio.htm` |
| Peak Confirmation Result | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_confirmationResult.htm` |
| Fluorescence Spectrum | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_flSpectrum.htm` |
| MSLS Hit | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_hitMassSpec.htm` |
| SLS Hit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_hitSpec.htm` |
| Confirmation peak excluded? | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_isExcluded.htm` |
| Isotopic Dot Product | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_isoDotProduct.htm` |
| ISTD Chromatogram | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_istdChm.htm` |
| ISTD Peak | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_istdPeak.htm` |
| Mass Accuracy | Peak Purity and Identification / Peptide Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massAccuracy.htm` |
| Mass Accuracy Mass | Peak Purity and Identification Variables | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massAccuracyMass.htm` |
| Peak Mass Spectrum Parameters | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_massSpectrum.htm` |
| Peak Purity Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_match.htm` |
| Number of MSLS Hit | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_nMSlsHits.htm` |
| Number of SLS Hits | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_nSlsHits.htm` |
| Peak Apex Alignment | Peak Purity and Identification Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_peakApexStdDev.htm` |
| Peak Purity Index | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_ppi.htm` |
| Peak Ratio Mean Value | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_ratio.htm` |
| Reference Spectrum Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_refMatch.htm` |
| Reference Mass Spectrum Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_refMsMatch.htm` |
| RSD Peak Purity Match | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_match.htm` |
| RSD Peak Purity Index | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_ppi.htm` |
| RSD Peak Ratio | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_rsd_ratio.htm` |
| Peak UV Spectrum | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_spectrum.htm` |
| Summed Charge State Confirming Peak Area | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_summedChargeStateConfirmingPeakArea.htm` |
| Summed Confirming Peak Area | Peak Purity and Identification Variable | `ReportVariables_CSH/RepVar_Peak_PurityAndIdentification_summedConfirmingPeakArea.htm` |
| Peak Results Category | The following table lists the available variables in the Peak Results category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_Results.htm` |
| Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_amount.htm` |
| Amount Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_amount_deviation.htm` |
| Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_area.htm` |
| Manually Assigned | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_assigned.htm` |
| Asymmetry | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_asymmetry.htm` |
| Capillary Electrophoresis Area (CE Area) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_ceArea.htm` |
| Concentration | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_concentration.htm` |
| Group | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_group.htm` |
| Group Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupAmount.htm` |
| Group Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupArea.htm` |
| Group Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_groupHeight.htm` |
| K' (Capacity Factor) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_kValue.htm` |
| Level Check | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_check.htm` |
| Level Tolerance High Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_high_amount.htm` |
| Level Tolerance High Response | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_high_response.htm` |
| Level Tolerance Low Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_low_amount.htm` |
| Level Tolerance Low Response | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_level_tolerance_low_response.htm` |
| Manipulated? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_modified.htm` |
| Statistical Moments | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_moment.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_name.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_number.htm` |
| Peak to Valley Ratio | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_peakToValleyRatio.htm` |
| Rank | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rank.htm` |
| Relative Amount/Area/CE Area/Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rel_amount.htm` |
| Relative Retention Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_rel_retention_time.htm` |
| Resolution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_resolution.htm` |
| Retention Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_deviation.htm` |
| Retention Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_time.htm` |
| Retention Window Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_retention_window.htm` |
| Retention Index | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_ri.htm` |
| Baseline/Signal Value at Peak Retention | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_sig_value_baseline.htm` |
| Skewness | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_skewness.htm` |
| Signal-to-Noise Ratio | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_sn.htm` |
| Detection Code at Peak Start or Peak End (AIA Peak Type) | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_detection_code.htm` |
| Peak Start/Stop Time | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_time.htm` |
| Baseline/Signal Value at Peak Start/End | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_start_value_baseline.htm` |
| Theoretical Plates | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_theoretical_plates.htm` |
| Type | In the Report Table, double-click a column header. | `ReportVariables_CSH/RepVar_Peak_Results_type.htm` |
| Width/Left Width/Right Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peak_Results_width.htm` |
| Signal to Noise Ratio | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SN.htm` |
| SN Intermediate Results | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate.htm` |
| Noise Value | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise.htm` |
| Noise End Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise_end_time.htm` |
| Noise Start Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_noise_start_time.htm` |
| Noise Regression Offset | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_offset.htm` |
| Ratio | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_ratio.htm` |
| Signal Value | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_signal.htm` |
| Noise Regression Slope | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediate_slope.htm` |
| Number of Noise Points | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_Peak_SNIntermediatenum_noise_points.htm` |
| CAS Number | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_Tentative_ID_CAS_Number.htm` |
| Peak Tentative Identification Category | The following table lists the available variables in the Peak Tentative Identification category, which is a sub-category of the Peak Purity and Identification category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peak_TentativeID.htm` |
| Amount | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Amount.htm` |
| Internal Standard Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_ISTD.htm` |
| Library Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_LibName.htm` |
| Match | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Match.htm` |
| Name | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Name.htm` |
| Probability | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_Probability.htm` |
| Reverse Match | Peak Tentative Identification Variable | `ReportVariables_CSH/RepVar_Peak_TentativeID_ReverseMatch.htm` |

### IntactDeconvolution

**Official Help topics:** 113

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Intact Protein Deconvolution Category | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution.htm` |
| Adduct Mass | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_AdductMass.htm` |
| Average Width RT | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_AveragingWidthRT.htm` |
| Biggest Gap RT | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_BiggestGapRT.htm` |
| Charge Carrier | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChargeCarrier.htm` |
| Charge Range High | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChargeHigh.htm` |
| Charge Range Low | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChargeLow.htm` |
| Choice of Peak Model Index | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChoiceOfPeakModelIndex.htm` |
| Chromatogram Parameters Category | Open the Chromatogram Parameters category by selecting the Chromatogram Parameters variable in the Intact Protein Deconvolution category. The variables in the Chromatogram Parameters category report information about the settings selected for the chromatogram displayed in the chromatogram pane of the Processing Method Editor. The following table lists the av | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChromatogramCategory.htm` |
| Chromatogram End Time | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChromatogramEndTime.htm` |
| Chromatogram Start Time | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChromatogramStartTime.htm` |
| Chromatogram Type | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ChromatogramType.htm` |
| Result Component Category | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component.htm` |
| Apex Retention Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ApexRt.htm` |
| Apex RT Percent CV | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ApexRtPercentCv.htm` |
| Charge State Count | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ChargeStateCount.htm` |
| High Charge State Range | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ChargeStateRangeHigh.htm` |
| Low Charge State Range | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ChargeStateRangeLow.htm` |
| Component ID | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ComponentId.htm` |
| Condition | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_Condition.htm` |
| Delta Mass | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_DeltaMass.htm` |
| Detected Interval Count | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_DetectedIntervalCount.htm` |
| Drug Load | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_DrugLoad.htm` |
| End Retention Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_EndRt.htm` |
| Fractional Abundance | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_FractionalAbundance.htm` |
| Intensity | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_Intensity.htm` |
| Intensity Percent CV | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_IntensityPercentCv.htm` |
| Mass | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_Mass.htm` |
| Mass Percent CV | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_MassPercentCv.htm` |
| Mass Std. Dev. | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_MassStdDev.htm` |
| Matched Charges Category | O pen the Matched Charges category by selecting the Matched Charges variable in the Intact Protein Deconvolution category. The variables in the Matched Charges category report information about results obtained when matching the measured masses of components detected by Chromeleon to the masses of target sequences specified by the user. The following table l | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_MatchedCharges.htm` |
| Matched Mass Error | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_MatchedMassError.htm` |
| Modification | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_Modification.htm` |
| Number of Files Observed | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_NumberOfFilesObserved.htm` |
| PPM Std. Dev. | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_PpmStdDev.htm` |
| Protein Name | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ProteinName.htm` |
| Relative Abundance | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_RelativeAbundance.htm` |
| High Retention Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_RtRangeHigh.htm` |
| Low Retention Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_RtRangeLow.htm` |
| High Scan Range | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ScanRangeHigh.htm` |
| Low Scan Range | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ScanRangeLow.htm` |
| Score | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_Score.htm` |
| Score Percent CV | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_ScorePercentCv.htm` |
| Start Retention Time | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_StartRt.htm` |
| Theoretical Mass | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_Component_TheoreticalMass.htm` |
| Result Component Count | Intact Protein Deconvolution Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ComponentCount.htm` |
| Consider Overlaps | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ConsiderOverlaps.htm` |
| Custom Distribution Table | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_CustomDistributionTblId.htm` |
| Deconvolution Algorithm | Intact Protein Deconvolution Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_DeconvolutionAlgorithm.htm` |
| Do Use Isotopic Profiles | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_DoUseIsotopicProfiles.htm` |
| End Scan Number | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_EndScanNumber.htm` |
| Expected Intensity Error | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ExpectedIntensityErr.htm` |
| Fit Factor | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_FitFactor.htm` |
| High Number Adjacent Charges | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_HighNumberAdjacentCharges.htm` |
| Intensity Threshold Scale | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_IntensityThresholdScale.htm` |
| Is Calculate XIC | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_IsCalculateXIC.htm` |
| Is High Sensitivity | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_IsHighSensitivity.htm` |
| Is Negative Ion | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_IsNegativeIon.htm` |
| Is PPM Tolerance | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_IsPpmTolerance.htm` |
| Low Number Adjacent Charges | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_LowNumberAdjacentCharges.htm` |
| Mass Range High | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MassRangeHigh.htm` |
| Mass Range Low | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MassRangeLow.htm` |
| Mass Tolerance | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MassTolerance.htm` |
| Charge | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_ChargeId.htm` |
| Delta Mass (Dalton) | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_DeltaMassDa.htm` |
| Delta Mass (ppm) | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_DeltaMassPpm.htm` |
| Fit Factor | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_FitFactor.htm` |
| Fit Factor Left | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_FitFactorLeft.htm` |
| Fit Factor Right | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_FitFactorRight.htm` |
| Intensity | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_Intensity.htm` |
| Measured mz | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_MeasuredMz.htm` |
| Most Abundant m/z | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_MatchedCharges_MostAbundantMz.htm` |
| Mass Tolerance | Multiconsensus Merge Parameters/Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MergeTolerance.htm` |
| Mass Tolerance Type | Multiconsensus Merge Parameters/Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MergeToleranceType.htm` |
| Min Cycles | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MinCycles.htm` |
| Minimum Charge States | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MinimumChargeStates.htm` |
| Minimum Required Occurrences | Multiconsensus Merge Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MinimumRequiredOccurrences.htm` |
| Min Intensity | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MinIntensity.htm` |
| Min Peak Significance | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_MinPeakSignificance.htm` |
| Multiconsensus Mass Parameters Category | Open the Multiconsensus Mass Parameters category by selecting the Multiconsensus Mass Parameters variable in the Intact Protein Deconvolution category. When t he multiconsensus result format is selected for experiments with multiple loaded raw data files, Chromeleon processes one experiment and then merges the deconvolution results from all of the loaded raw | `ReportVariables_CSH/RepVar_IntactDeconvolution_MulticonsensusMergeCategory.htm` |
| Negative Charge | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_NegativeCharge.htm` |
| Noise Compensation | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_NoiseCompensation.htm` |
| Noise Rejection | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_NoiseRejection.htm` |
| Number of Peak Models | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_NumberOfPeakModels.htm` |
| Offset Percent | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OffsetPercent.htm` |
| Offset Scans | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OffsetScans.htm` |
| Offset Type | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OffsetType.htm` |
| Output Mass High | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OutputMassHigh.htm` |
| Output Mass Limit High | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OutputMassLimitHigh.htm` |
| Output Mass Limit Low | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OutputMassLimitLow.htm` |
| Output Mass Low | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OutputMassLow.htm` |
| Output Mass Type | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_OutputMassType.htm` |
| Peak Model Width Scale | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_PeakModelWidthScale.htm` |
| Quality Score Threshold | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_QualityScoreThreshold.htm` |
| Range Display Type | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RangeDisplayType.htm` |
| Relative Abundance Threshold | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RelativeAbundanceThreshold.htm` |
| Relative Intensity Threshold | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RelativeIntensityThreshold.htm` |
| Remainder Threshold | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RemainderThreshold.htm` |
| Resolution at 400 | ReSpect Parameters/Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ResolutionAt400.htm` |
| ReSpect Parameters Category | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_ReSpectCategory.htm` |
| Restricted Time | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RestrictedTime.htm` |
| Rt Tolerance | Multiconsensus Merge Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_RtTolerance.htm` |
| Start Time | Sliding Windows Parameter Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_SlidingStartTime.htm` |
| Stop Time | Sliding Windows Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_SlidingStopTime.htm` |
| Sliding Windows Parameters Category | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_SlidingWindowCategory.htm` |
| Source Spectrum Algorithm | Intact Protein Deconvolution Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_SourceSpectrumAlgorithm.htm` |
| Start Scan Number | Chromatogram Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_StartScanNumber.htm` |
| Target Peak Mass | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_TargetPeakMass.htm` |
| Target Peak Shape Left | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_TargetPeakShapeL.htm` |
| Target Peak Shape Right | ReSpect Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_TargetPeakShapeR.htm` |
| Threshold SN | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_ThresholdSNId.htm` |
| Xtract Parameters Category | Open the Report Column dialog box of the component table (for example, by double-clicking a column header in the component table). | `ReportVariables_CSH/RepVar_IntactDeconvolution_XtractCategory.htm` |
| Charge Carrier Type | Xtract Parameters Variable | `ReportVariables_CSH/RepVar_IntactDeconvolution_XtractChargeCarrierType.htm` |

### NonTargetedMS 

**Official Help topics:** 48

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Non-Targeted MS Processing (SIEVE) Category | To access these variables: | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE.htm` |
| Algorithm | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Algorithm.htm` |
| Alignment Bypass | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_AlignmentBypass.htm` |
| Alignment Min Intensity | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_AlignmentMinIntensity.htm` |
| Correlation Bin Width | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_CorrelationBinWidth.htm` |
| Description | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Description.htm` |
| Frame Category | Non-Targeted MS Processing (SIEVE) Category | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame.htm` |
| Avg Intensity | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_AvgIntensity.htm` |
| Base Component | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_BaseComponent.htm` |
| Charge | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_Charge.htm` |
| Component ID | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_ComponentId.htm` |
| Component Score | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_ComponentScore.htm` |
| Frame ID | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_FrameId.htm` |
| Mass | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_Mass.htm` |
| Molecular Weight | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_MolecularWeight.htm` |
| Pattern Recognition Element | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_PatternRecognitionElement.htm` |
| Pattern Recognition Root | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_PatternRecognitionRoot.htm` |
| Pattern Recognition Size | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_PatternRecognitionSize.htm` |
| Ratio | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_Ratio.htm` |
| Reference Avg Intensity | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_ReferenceAvgIntensity.htm` |
| Retention Time | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_RetentionTime.htm` |
| Weighted Mass | Use any of the methods for opening the Formula page of the Report Variable Properties dialog and invoke the Report Formula Editor . | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Frame_WeightedMass.htm` |
| Maximum Frames | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_MaximumFrames.htm` |
| Max Retention Time Shift | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_MaxRetentionTimeShift.htm` |
| Max Threads | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_MaxThreads.htm` |
| m/z Max | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_mzMax.htm` |
| m/z Min | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_mzMin.htm` |
| m/z Width | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_mzWidth.htm` |
| Name | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Name.htm` |
| Peak Intensity Threshold | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_PeakIntensityThreshold.htm` |
| Peak Threshold Percentage | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_PeakThresholdPct.htm` |
| Peak Threshold Peak Type | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_PeakThresholdPeakType.htm` |
| Peak Threshold Type | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_PeakThresholdType.htm` |
| Reference Index | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_ReferenceIndex.htm` |
| Reference Mode | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_ReferenceMode.htm` |
| Reference URI | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_ReferenceURI.htm` |
| Result Status | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_ResultStatus.htm` |
| RT Alignment Limits | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_RTAlignmentLimits.htm` |
| Scan Filters | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_ScanFilters.htm` |
| Tile Increment | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TileIncrement.htm` |
| Tile Maximum | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TileMaximum.htm` |
| Tile Size | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TileSize.htm` |
| Tile Threshold | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TileThreshold.htm` |
| Time Start | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TimeStart.htm` |
| Time Stop | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TimeStop.htm` |
| Time Width | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_TimeWidth.htm` |
| Type | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Type.htm` |
| Version | Non-Targeted MS Processing (SIEVE) Variable | `ReportVariables_CSH/RepVar_NonTargetedMS_SIEVE_Version.htm` |

### DetectionParameter

**Official Help topics:** 46

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Detection Parameters | The Detection Parameters category includes variables that give information about the value set in the processing method for the related detection parameter at a defined retention time (detection parameters can be set on the Detection tab page in the Processing Method Editor). A variable will only be listed if it is a variable of the detection algorithm set i | `ReportVariables_CSH/RepVar_DetectionParameter.htm` |
| Bunch Size (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasBunchSize.htm` |
| End Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasEndThreshold.htm` |
| End Trend (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasEndTrend.htm` |
| Force Baseline (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasForceBase.htm` |
| Shoulder Sensitivity (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasShoulder.htm` |
| Skim Sensitivity (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasSkimSens.htm` |
| Start Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasStartThreshold.htm` |
| Start Trend (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasStartTrend.htm` |
| Suppress (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasSuppress.htm` |
| Threshold (Atlas) | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_atlasThreshold.htm` |
| Baseline Noise Auto Range | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineNoiseAutoRange.htm` |
| Baseline Noise Start/End Time | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineStartTime.htm` |
| Baseline Type | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_baselineType.htm` |
| Consider Void Peak | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_considerVoidPeak.htm` |
| Detect Shoulder Peaks | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_detShoulderPeaks.htm` |
| Peak Slice | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_filter.htm` |
| Fronting Sensitivity Factor | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_frontFac.htm` |
| Front Riders to Main Peak | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_frontRiderToMain.htm` |
| Has a Fixed Baseline? | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_hasFixedBaseline.htm` |
| Part of Peak Group? | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_isInGruop.htm` |
| Lock Baseline | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_lockBl.htm` |
| Maximum Area Reject | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxAreaRj.htm` |
| Maximum Height Reject | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxHeightRj.htm` |
| Maximum Width | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_maxWidth.htm` |
| Minimum Area | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minArea.htm` |
| Minimum Baseline Box Width | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minBaselineBoxWidth.htm` |
| Minimum Height | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minHeight.htm` |
| Minimum Relative Area | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRelativeArea.htm` |
| Minimum Relative Height | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRelativeHeight.htm` |
| Minimum Rider Ratio | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minRiderRatio.htm` |
| Minimum Signal To Noise Ratio | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minSignalNoiseRatio.htm` |
| Minimum Width | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_minWidth.htm` |
| Detect Negative Peaks | Detection / MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_negDetect.htm` |
| Inhibit Integration | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_noInteg.htm` |
| Sensitivity | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_noise.htm` |
| Rider Detection | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderDetection.htm` |
| Rider Threshold | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderMin.htm` |
| Maximum Rider Ratio | (MS) Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderRatio.htm` |
| Rider Skimming | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_riderSkim.htm` |
| Peak Shoulder Threshold | Detection Parameters Variable | `ReportVariables_CSH/RepVar_DetectionParameter_shoulderThrshld.htm` |
| Cobra Smoothing Width | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_smoothingWidth.htm` |
| Snap Baseline | Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_snapBaseline.htm` |
| Tailing Sensitivity Factor | MS Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_tailFac.htm` |
| Valley to Valley | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_valval.htm` |
| Void Volume Treatment | (MS) Detection Parameter Variable | `ReportVariables_CSH/RepVar_DetectionParameter_voidVolumeTreatment.htm` |

### Component

**Official Help topics:** 45

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Component Category | The Component category includes variables that provide information about the values in the component table of the processing method. The following table lists the available variables in the Component category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Component.htm` |
| Amount | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_amount.htm` |
| Concentration Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_amount_unit.htm` |
| Manual C0/C1/C2/C3 | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_C0.htm` |
| Calculated Mass | Injection Variable/Component Variable | `ReportVariables_CSH/RepVar_Component_calculated_mass.htm` |
| Calibration Type | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_calibration_type.htm` |
| CAS ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_casNumber.htm` |
| Channel | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_channel.htm` |
| Charge | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_charge.htm` |
| Chemical Formula | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_chemFormula.htm` |
| Comment | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_comment.htm` |
| Lower/Upper Confidence Probability | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_confLowerProbability.htm` |
| Group | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_group.htm` |
| Group Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_grouptype.htm` |
| Include Identified Peak | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_includeidentifiedpeak.htm` |
| Individual MS Detection Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_indvMsDet.htm` |
| Evaluation Type | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_integration_type.htm` |
| Left Limit/Right Limit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_left_limit.htm` |
| Level Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance.htm` |
| Level Tolerance High Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance_high_amount.htm` |
| Level Tolerance Low Amount | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_level_tolerance_low_amount.htm` |
| Molecular Mass | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_massToChargeRatio.htm` |
| Mass Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_massTolerance.htm` |
| MS Detection Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_MsDetectionParameters.htm` |
| MS Extraction Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_msExt.htm` |
| Name | Component Variable/Peak Group Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_name.htm` |
| Number | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_number.htm` |
| Peptide Group | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_peptideGroup.htm` |
| Reference Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_reference_spectrum.htm` |
| Reference Mass Spectrum Settings | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_RefMsSettings.htm` |
| Factor | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_response_factor.htm` |
| Retention Time | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_retention_time.htm` |
| Retention Time Interpretation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_retention_type.htm` |
| Retention Index | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_ri.htm` |
| Check Extrema | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_check_extrema.htm` |
| Match Criterion | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_compare_method.htm` |
| Spectrum Derivative | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_derivative.htm` |
| Minimum/Maximum Wavelength | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_max_wavelength.htm` |
| Relative Maximum Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_relmaxdev.htm` |
| Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_spec_threshold.htm` |
| Standard Method | Component/Peak Group Variable | `ReportVariables_CSH/RepVar_Component_standard_method.htm` |
| Peak Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_type.htm` |
| Previous Retention | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_use_previous_rettime.htm` |
| Window/(Component) Identification | Component Variable/Peptide Variable | `ReportVariables_CSH/RepVar_Component_window.htm` |
| XIC Detection Reference Rule | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Component_xicdetectionreferencerule.htm` |

### ProcessingMethod

**Official Help topics:** 45

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Processing Method Category | The Processing Method category includes variables that provide information about settings selected in the Processing Method . The following table lists the variables available in the Processing Method category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_ProcessingMethod.htm` |
| Available Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_availAlgVer.htm` |
| Blank Run Injection Record | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_blankRunInjection.htm` |
| Subtraction Mode | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_blankRunSubtraction.htm` |
| Calibration Level Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_calLevelName.htm` |
| Calibration Mode | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_calMode.htm` |
| Comment | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_comment.htm` |
| Creation Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_creation_operator.htm` |
| Creation Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_creation_time.htm` |
| Curve Fitting | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_curveFitting.htm` |
| Data Vault | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_dataVault.htm` |
| Dead Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_deadTime.htm` |
| Delay Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_delayTime.htm` |
| Delay Time Detector | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_delayTimeDetector.htm` |
| Detection Algorithm | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_detAlgorithm.htm` |
| Directory | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_directory.htm` |
| Effective Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_effAlgVer.htm` |
| Origin of Fixed Calibration Standards | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_fixedCalibrationStandardsOrigin.htm` |
| Last Fixed Calibration Update Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_FixedCalibrationUpdateOperator.htm` |
| Last Fixed Calibration Update Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_FixedCalibrationUpdateTime.htm` |
| Is Latest Algorithm Version | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_isLatestAlgVer.htm` |
| Matrix Correction Enabled | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_matrixCorrection.htm` |
| MS Library Screening Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_msls.htm` |
| MS Settings | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_MsSettings.htm` |
| Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_name.htm` |
| Number of Calibration Levels | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfCalLevels.htm` |
| Number of Components | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfComponents.htm` |
| Number of Detection Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfDetParams.htm` |
| Number of Peak Groups | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_numOfPeakGroups.htm` |
| Select Peak Group | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_PeakGroup.htm` |
| Peak Width Determination | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_peakWidthDetermination.htm` |
| MS Detection Algorithm | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_procMeth.msDetAlgorithm.htm` |
| Reference Inject Volume | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_referenceInjectVolume.htm` |
| Retention Time Determination | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_retTimeDetermination.htm` |
| Select Component in the Component Table | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_selectComponent.htm` |
| Separate Calibration | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sepCalibration.htm` |
| Parent Sequence Name | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_seqName.htm` |
| Parent Sequence Header Record | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sequence.htm` |
| Spectra Library Screening Parameters | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sls.htm` |
| Number of Test Cases | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sst_rows.htm` |
| Select Test Case | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_sst_tc.htm` |
| Last Update Operator | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_update_operator.htm` |
| Last Update Date & Time | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_update_time.htm` |
| Use Amount Ratio for Var. ISTD | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_useAmountRatioForVarIstd.htm` |
| UV Spectra Settings | Processing Method Variable | `ReportVariables_CSH/RepVar_ProcessingMethod_uv_settings.htm` |

### Sequence

**Official Help topics:** 43

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Sequence Category | The Sequence category includes variables that give information about the sequence. The following table lists the available variables in the Sequence category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Sequence.htm` |
| Add To Queue Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_addToQueue_Operator.htm` |
| Approve Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveComment.htm` |
| Approve Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveOperator.htm` |
| Approve Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_approveTime.htm` |
| Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_comment.htm` |
| Created by Qualification | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_createdByQualification.htm` |
| Creation Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_creation_operator.htm` |
| Creation Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_creation_time.htm` |
| Data Vault | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_dataVault.htm` |
| Default Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultChannel.htm` |
| Default Report Template | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultReportDefinition.htm` |
| Default View Settings | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_defaultViewSettings.htm` |
| Directory | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_directory.htm` |
| eWorkflow Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_eWorkflowName.htm` |
| Imported Data | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_imported.htm` |
| Displaying Imported Results | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_importedResults.htm` |
| Include Canceller | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeCanceller.htm` |
| Include Creator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeCreator.htm` |
| Include Queue Starter | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_includeQueueStarter.htm` |
| Select Injection | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_injection.htm` |
| Instrument | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_instrument.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_name.htm` |
| Number of Injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_nInjections.htm` |
| Notifications Enabled | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notificationsEnabled.htm` |
| Notify Aborted Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyAbortedRecipient.htm` |
| Notify Cancelled Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyCancelledRecipient.htm` |
| Notify Finished Recipient | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifyFinishedRecipient.htm` |
| Notify Sequence Aborted | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceAborted.htm` |
| Notify Sequence Cancelled | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceCancelled.htm` |
| Notify Sequence Finished | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_notifySequenceFinished.htm` |
| NTMS New Peak Detection Algorithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_NTMSPeakDetectionAlgorithm.htm` |
| Peptide Display Mode | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_peptideDisplayMode.htm` |
| Review Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewComment.htm` |
| Review Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewOperator.htm` |
| Review Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_reviewTime.htm` |
| Required Signature Steps | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_signatureSteps.htm` |
| Signature Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_signStatus.htm` |
| Submit Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitComment.htm` |
| Submit Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitOperator.htm` |
| Submit Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_submitTime.htm` |
| Last Update Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_update_operator.htm` |
| Last Update Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Sequence_update_time.htm` |

### Chromatogram

**Official Help topics:** 40

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Chromatogram Category | The following table lists the available variables in the Chromatogram category. Click a variable name to read the full description. Some variables can only be used if the Cobra detection algorithm was selected. | `ReportVariables_CSH/RepVar_Chromatogram.htm` |
| Auto Noise | In the Chromeleon Studio, navigate into the Report Designer category. | `ReportVariables_CSH/RepVar_Chromatogram_autoNoise.htm` |
| Baseline Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_baselineThreshold.htm` |
| Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_channel.htm` |
| Count Peaks if ... | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_countif.htm` |
| Curvature | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_curvature.htm` |
| Curvature Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_curvatureNoise.htm` |
| Delay Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_delayTime.htm` |
| Detection Algorithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detAlgorithm.htm` |
| Detection Reference XIC? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detectionreferencexic.htm` |
| Detector | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_detector.htm` |
| Signal Drift | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_drift.htm` |
| Effective Min. Peak Area | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effMinArea.htm` |
| Effective Min. Peak Height | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effMinHeight.htm` |
| Effective Smoothing Width | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_effSmoothingWidth.htm` |
| End Time (relative to Inject Time) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_end_time.htm` |
| Fluorescence Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_flSpectrum.htm` |
| Import Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_import_type.htm` |
| Modification Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manip_operator.htm` |
| Modification Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manip_time.htm` |
| Manipulated? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_manipulated.htm` |
| Mass Detected | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_mass_detected.htm` |
| Mass Spectrum Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_massSpectrum.htm` |
| Metadata | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_metadata.htm` |
| MS Signal Extraction Parameters | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_msExt.htm` |
| Signal Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_noise.htm` |
| Noise Determination Range Start/End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_noiseDetStart.htm` |
| Number of Peaks | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_npeaks.htm` |
| Select Peak | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_peak.htm` |
| Peak Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_peakThreshold.htm` |
| Sample Rate | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sig_rate.htm` |
| Sample Step | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sig_step.htm` |
| Signal Description | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalDesc.htm` |
| Signal Statistic | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalStatistic.htm` |
| Signal Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalUnit.htm` |
| Signal Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_signalValue.htm` |
| Slope | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_slope.htm` |
| Start Time (relative to Inject Time) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_start_time.htm` |
| Sum Peak Results if ... | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_sumif.htm` |
| UV Spectrum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Chromatogram_uvSpectrum.htm` |

### Injection

**Official Help topics:** 35

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Injection Category | The Injection category includes variables that give information about the injection taken from the columns of the injection list. The following table lists the available variables in the Injection category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Injection.htm` |
| Adduct Masses | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_adduct_masses.htm` |
| Adducts | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_adducts.htm` |
| IntStd | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_amount.htm` |
| AutoDilution Ratio | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_autodilution_ratio.htm` |
| Level | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_calLevel.htm` |
| Chemical Formula and Adduct Masses | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chemical_formula_and_adduct_masse.htm` |
| Chemical Formula and Adducts | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chemical_formula_and_adducts).htm` |
| Select Chromatogram | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_chm.htm` |
| Comment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_comment.htm` |
| Dilution Factor | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_dilution_factor.htm` |
| GUID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_guid.htm` |
| ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_id.htm` |
| Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_inject_volume.htm` |
| Level Check | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_level_check.htm` |
| Lock Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_lockStatus.htm` |
| Lock Version | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_lockVersion.htm` |
| Processing Method | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_method.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_name.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_number.htm` |
| Position | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_position.htm` |
| Instrument Method | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_program.htm` |
| Reference Retention Time Standard | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Reference_Retention_Time_Standard.htm` |
| Relative Position | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_relativePosition.htm` |
| Replicate ID | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_replicate.htm` |
| Retention Time Standard Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Retention_Time_Standard_Error.htm` |
| Retention Time Standard Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_Retention_Time_Standard_Status.htm` |
| Weight | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sample_weight.htm` |
| Spike Group | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_spike_group.htm` |
| Number of Re-injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_num_reinjects.htm` |
| Test Case Overall Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_result .htm` |
| Test Case Specific Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_sst_tc_result.htm` |
| Status | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_status.htm` |
| Inject Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_time.htm` |
| Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Injection_type.htm` |

### HitSpectrum

**Official Help topics:** 24

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Hit Spectrum Category | Open the Hit Spectrum category, for example, by selecting the SLS Hit variable of the Peak Purity and Identification category. It includes variables that retrieve information stored in the = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/Glossary_Spectral_Library.htm');return f | `ReportVariables_CSH/RepVar_HitSpectrum.htm` |
| Acquisition Step | The Acquisition Step variable returns the sample rate that was used to record the spectrum. | `ReportVariables_CSH/RepVar_HitSpectrum_acqStep.htm` |
| Comment | The Comment variable returns the comment that is registered in the spectral library for the library spectrum. | `ReportVariables_CSH/RepVar_HitSpectrum_comment.htm` |
| Detector Name | The Detector Name variable returns the name of the detector with which the library spectrum was recorded. | `ReportVariables_CSH/RepVar_HitSpectrum_detName.htm` |
| Detector Serial Number | The Detector Serial Number returns the serial number of the detector with which the library spectrum was recorded. | `ReportVariables_CSH/RepVar_HitSpectrum_detSerNo.htm` |
| Extract Date/Time | The Extract Date/Time variable returns the date and time when the library spectrum was extracted and saved to the spectral library. | `ReportVariables_CSH/RepVar_HitSpectrum_extrTime.htm` |
| Extract User Name | The Extract User Name variable returns the name of the user who extracted the library spectrum and saved it to the spectral library. | `ReportVariables_CSH/RepVar_HitSpectrum_extrUser.htm` |
| ID | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_ID.htm` |
| Injection | The Injection variable returns the properties of the injection from which the library spectrum was extracted. Note that this variable cannot be evaluated if the injection was deleted. | `ReportVariables_CSH/RepVar_HitSpectrum_injection.htm` |
| Injection Name | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_injName.htm` |
| Data Acquisition Date/Time | The Data Acquisition Date/Time variable returns the acquisition time when the library spectrum was originally recorded. | `ReportVariables_CSH/RepVar_HitSpectrum_injTime.htm` |
| Injection Url | The Injection Url variable returns the name of the injection from which the extracted library spectrum was taken. | `ReportVariables_CSH/RepVar_HitSpectrum_injUrl.htm` |
| Instrument Method | If an injection was processed automatically using an instrument method, the Instrument Method variable returns the name of the instrument method file used to acquire the spectrum. | `ReportVariables_CSH/RepVar_HitSpectrum_instMethod.htm` |
| Instrument Name | The Instrument Name variable returns the name of the Instrument for which the library spectrum was recorded. | `ReportVariables_CSH/RepVar_HitSpectrum_instrument.htm` |
| Library Name | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_libName.htm` |
| Match Factor | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_match.htm` |
| Component Name | The Component Name variable returns the name of the component from the spectral library. | `ReportVariables_CSH/RepVar_HitSpectrum_name.htm` |
| Number of Relative Extrema | The Number of Relative Extrema variable creates a column that indicates the number of relative extrema that are registered for the library spectrum in the spectral library. | `ReportVariables_CSH/RepVar_HitSpectrum_nExtrema.htm` |
| Retention Index | The Retention Index variable returns the value for the retention index that was entered in the spectral library for this spectrum. It can be used for comparison of retention times of different chromatographic systems. | `ReportVariables_CSH/RepVar_HitSpectrum_retIndex.htm` |
| Retention Time | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_retTime.htm` |
| Sequence Name | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_seqName.htm` |
| Sequence Header Record | The Sequence Header Record variable returns selected information about the sequence from which the spectrum was extracted. Note that this variable cannot be evaluated if the sequence was deleted or moved to a different location. | `ReportVariables_CSH/RepVar_HitSpectrum_sequence.htm` |
| Solvent Composition | The Solvent Composition variable returns the solvent or solvents used for the library spectrum. | `ReportVariables_CSH/RepVar_HitSpectrum_solvents.htm` |
| Spectrum Data | Hit Spectrum and Library Spectrum Variable | `ReportVariables_CSH/RepVar_HitSpectrum_specData.htm` |

### MsDetectionParameters

**Official Help topics:** 24

| Variable / topic | Help summary | Help topic |
|---|---|---|
| MS Detection Parameters | The MS Detection Parameters category includes variables that give information about the value set in the processing method for the related detection parameter at a defined retention time. A variable will only be listed if it is a variable of the detection algorithm set in the = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" cl | `ReportVariables_CSH/RepVar_MsDetectionParameters.htm` |
| Algorithm | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_algorithm.htm` |
| Area Noise Factor | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_areaNoiseFac.htm` |
| Area Scan Window | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_areaScanWin.htm` |
| Area Tail Extension | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_areaTailExt.htm` |
| Baseline Noise Rejection Factor | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_bslineNoiseRjFac.htm` |
| Baseline Noise Tolerance | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_bslineNoiseTolerance.htm` |
| Baseline Window | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_bslineWin.htm` |
| Calculate Noise As | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_calcNoiseAs.htm` |
| Constrain Peak Width | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_cstrPeakWidth.htm` |
| Enable Valley Detection | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_enableValDet.htm` |
| Expected Width | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_expWidth.htm` |
| Minimum Scans in Baseline | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_minBslineScans.htm` |
| Minimum Peak Width | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_minPeakWidth.htm` |
| Multiplet Resolution | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_multipletRes.htm` |
| Noise Method | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_noiseMeth.htm` |
| Peak Height | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_peakHeight.htm` |
| Peak Noise Factor | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_peakNoiseFac.htm` |
| Peak S/N Cutoff | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_peakSnCutoff.htm` |
| Rise Percentage | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_risePct.htm` |
| RMS | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_rms.htm` |
| S/N Threshold | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_snThreshold.htm` |
| Tailing Factor | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_tailingFac.htm` |
| Valley Depth | MS Detection Parameters Variable | `ReportVariables_CSH/RepVar_MsDetectionParameters_valDepth.htm` |

### MS 

**Official Help topics:** 23

| Variable / topic | Help summary | Help topic |
|---|---|---|
| MS Extraction Parameters Category | The variables in the MS Extraction Parameters category report information about the defined MS extraction settings for a component on the Extracted Ion Chromatograms tab page of the Component Table Properties dialog box of the Processing Method Editor . The following table lists the available variables in the category. Click a variable name to read the full  | `ReportVariables_CSH/RepVar_MS_Extraction.htm` |
| Collision Energy | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_collisionEnergy.htm` |
| End Time | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_endTime.htm` |
| Extraction Time | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_extractionTime.htm` |
| Extraction Window | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_extractionWindow.htm` |
| Auto Filter | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_filter.htm` |
| Include in Calibration | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_includeInCalibration.htm` |
| Ion Coelution | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_ionCoelution.htm` |
| Mass Ranges | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_massRanges.htm` |
| Number of Smoothing Points | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_nSmoothingPoints.htm` |
| Precursor Mass | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_precursorMass.htm` |
| Ratio Enabled | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_ratioEnabled.htm` |
| Ratio Window | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_ratioWindow.htm` |
| Ratio Window Type | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_ratioWindowType.htm` |
| Smoothing Algorithm | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_smoothingAlgorithm.htm` |
| Start Time | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_startTime.htm` |
| Target Ratio | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_targetRatio.htm` |
| Trace Type | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_traceType.htm` |
| Use Default Smoothing | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_useDefaultSmoothing.htm` |
| Use Retention Time | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_useRetentionTime.htm` |
| Use Retention Window | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Extraction_useRetentionWindow.htm` |
| MS Signal Extraction Parameters Category | Variables in the MS Signal Extraction Parameters category report information about values from the acquired raw signal data. The following table lists the available variables in the category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_MS_Signal_Extraction.htm` |
| Evaluation Type | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MS_Signal_Extraction_evaluationType.htm` |

### MS LS

**Official Help topics:** 22

| Variable / topic | Help summary | Help topic |
|---|---|---|
| MS Library Screening Category | Open the MS Library Screening category by selecting the MS Library Screening Parameters variable of the Processing Method category. The variables in the MS Library Screening category report information about the settings selected on the MS Library Screening dialog box of the Processing Method Editor. The following table lists the available variables in the c | `ReportVariables_CSH/RepVar_MSLS.htm` |
| MS Library Screening Hit Category | The variables in the MS Library Screening Hit category report information about the matching mass spectra (hits) found during MS library screening. This is not a stand-alone category; the variables in this category are always appended to the MSLS Hit variable of the Peak Purity and Identification category . | `ReportVariables_CSH/RepVar_MSLS_hit.htm` |
| CAS Number | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitCasNumber.htm` |
| Chemical Formula | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitChemicalFormula.htm` |
| Intensity | Mass Spectrum Variable/MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitIntensity.htm` |
| Library Name | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitLibraryName.htm` |
| Mass | Mass Spectrum Variable/ MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitMass.htm` |
| Match Factor | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitMatchFactor.htm` |
| Molecular Weight | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitMolecularWeight.htm` |
| Name | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitName.htm` |
| Probability | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitProbability.htm` |
| Reverse Match Factor | MS Library Screening Hit Variable | `ReportVariables_CSH/RepVar_MSLS_hitReverseMatchFactor.htm` |
| Is MS Library Used | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_isLibraryUsed.htm` |
| MS Library | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_library.htm` |
| Number of MS Libraries | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_libraryCount.htm` |
| Match Threshold | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_matchThreshold.htm` |
| Mol. Weight | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_molWeight.htm` |
| Probability Threshold | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_probabilityThreshold.htm` |
| Reverse Match Threshold | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_reverseMatchThreshold.htm` |
| Reverse Search | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_reverseSearch.htm` |
| Search Type | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_searchType.htm` |
| Search with Mol. Weight | MS Library Screening Variable | `ReportVariables_CSH/RepVar_MSLS_searchWithMolWeight.htm` |

### NTMS BioPharmaFinder

**Official Help topics:** 22

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Non-Targeted MS Processing (BioPharma Finder) Category | To access these variables: | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder.htm` |
| Component Results Category | Non-Targeted MS Processing (BioPharma Finder) Category | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent.htm` |
| Average Mass Exp | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_AverageMassExp.htm` |
| Charge State | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ChargeState.htm` |
| Component Number | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ComponentNumber.htm` |
| Control Avg Mass Exp | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlAvgMassExp.htm` |
| Control Charge State | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlChargeState.htm` |
| Control Mono Mass Exp | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlMonoMassExp.htm` |
| Control MS Area | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlMSArea.htm` |
| Control M/Z | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlMZ.htm` |
| Control RT (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlRT.htm` |
| Control RT Start (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlRTStart.htm` |
| Control RT Stop (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_ControlRTStop.htm` |
| Max MS Area | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_MaxMSArea.htm` |
| Mono Mass Exp | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_MonoMassExp.htm` |
| MS Area | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_MSArea.htm` |
| MS Area Ratio | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_MSAreaRatio.htm` |
| M/Z | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_MZ.htm` |
| RT (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_RT.htm` |
| RT Start (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_RTStart.htm` |
| RT Stop (min) | Non-targeted MS Processing Variable (BioPharma Finder) | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultComponent_RTStop.htm` |
| Result Status | Non-Targeted MS Processing (BioPharma Finder) Variable | `ReportVariables_CSH/RepVar_NTMSBioPharmaFinder_ResultStatus.htm` |

### CompositeScoring

**Official Help topics:** 21

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Amount Ratio Confirmation Channel | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_amountRatioConfirmationChannel.htm` |
| Amount Ratio Reference Channel | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_amountRatioRefChannel.htm` |
| Amount Ratio Tolerance Percentage | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_amountRatioTolerance.htm` |
| Is Amount Ratio Used | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_amountRatioUsed.htm` |
| Peak Apex Alignment Type | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_apexAlignmentType.htm` |
| Peak Apex Align Threshold | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_apexAlignThreshold.htm` |
| Is Apex Align Used | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_apexAlignUsed.htm` |
| Is Confirming Ion Ratio Used | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_confIonRatioUsed.htm` |
| Isotopic Dot Product Threshold | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_dotProductThreshold.htm` |
| Is Dot Product Used | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_dotProductUsed.htm` |
| Fail Threshold | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_failThreshold.htm` |
| Filter Isotope Reference Percentage | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_filterIsotopeReferencePct.htm` |
| Filter Isotope Reference Type | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_filterIsotopeReferenceType.htm` |
| Filter Isotope Reference Value | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_filterIsotopeReferenceValue.htm` |
| Filter Isotopes | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_filterIsotopes.htm` |
| IPD Component Query Rules | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_ipdComponentQueryRules.htm` |
| Mass Accuracy Calculation Type | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_massAccuracyCalculationType.htm` |
| Mass Accuracy Threshold | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_massAccuracyThreshold.htm` |
| Mass Accuracy Unit | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_massAccuracyUnit.htm` |
| Is Mass Accuracy Used | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_massAccuracyUsed.htm` |
| Pass Threshold | Processing Method Composite Scoring Variables | `ReportVariables_CSH/RepVar_CompositeScoring_passThreshold.htm` |

### Spectrum

**Official Help topics:** 20

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Spectrum Category | Open the Spectrum category (for example, by selecting the Peak UV Spectrum or Fluorescence Spectrum variable in the Peak Purity and Identification or Chromatogram category). The variables in the Spectrum category provide information about the properties of the spectrum. The following table lists the available variables in the Spectrum category. Click a varia | `ReportVariables_CSH/RepVar_Spectrum.htm` |
| Baseline Corrected | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_baselineCorrected.htm` |
| Baseline Correction | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_baselineCorrectionInfo.htm` |
| Statistical Moment | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_moment.htm` |
| Number of relative Extrema | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_nExtrema.htm` |
| Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_noise.htm` |
| Property Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_propertyUnit.htm` |
| Property Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_propertyValue.htm` |
| Retention Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_retTime.htm` |
| Scan Resolution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanInc.htm` |
| Scan Index | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanIndex.htm` |
| Scan Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanMax.htm` |
| Scan Minimum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanMin.htm` |
| Scan Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanUnit.htm` |
| Scan Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_scanValue.htm` |
| Signal Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_sigMax.htm` |
| Signal Minimum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_sigMin.htm` |
| Signal Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_sigUnit.htm` |
| Signal Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_sigValue.htm` |
| Restrict Wavelength Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Spectrum_subRange.htm` |

### MsSettings

**Official Help topics:** 19

| Variable / topic | Help summary | Help topic |
|---|---|---|
| MS Settings Category | Open the MS Settings category by selecting the MS Settings variable of the Processing Method category. The variables in the MS Settings category report information about the settings selected on the MS Settings tab page of the Processing Method Editor. The following table lists the available variables in the category. Click a variable name to read the full d | `ReportVariables_CSH/RepVar_MsSettings.htm` |
| Absolute Noise Reduction Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_absolutethreshold.htm` |
| Baseline Correction | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_baseline_correction.htm` |
| Maximum of Fixed Baseline Correction Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_fixed_blcorrection_range_max.htm` |
| Minimum of Fixed Baseline Correction Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_fixed_blcorrection_range_min.htm` |
| Fixed Noise Reduction Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_fixed_threshold.htm` |
| Inhibit Integration for TIC | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_inhibitIntegrationForTIC.htm` |
| Left Region Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_left_region_bunch.htm` |
| Manually Defined Mass Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_manuallyMassTolerance.htm` |
| Specify Mass Tolerance per Component | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_mass_tolerance_per_component.htm` |
| Global Mass Tolerance | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_massTolerance.htm` |
| Mass Tolerance Unit | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_massToleranceUnit.htm` |
| Noise Reduction Mode | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_noise_reduction.htm` |
| Number of Smoothing Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_nSmoothingPoints.htm` |
| Peak Spectrum Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_peak_spectrum_bunch.htm` |
| Relative Noise Reduction Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_relative_threshold.htm` |
| Right Region Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_right_region_bunch.htm` |
| Smoothing Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_smoothingType.htm` |
| Use Chemical Formula for Isotopic Distribution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MsSettings_useChemFormulaIsotopicDistribution.htm` |

### DataAuditTrail

**Official Help topics:** 18

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Data Audit Trail Category | The Data Audit Trail category includes variables that give information about the values in the Data Audit Trail Report table. The following table lists the available variables in the Data Audit Trail category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_DataAuditTrail.htm` |
| Additional Information | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_additional_information.htm` |
| Comment | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_comment.htm` |
| Show Details | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details.htm` |
| New Value (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_newvalue.htm` |
| Number (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_number.htm` |
| Object Path (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_objectpath.htm` |
| Old Value (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_oldvalue.htm` |
| Operation (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_operation.htm` |
| Property (details sub-category) | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_details_property.htm` |
| Object Name | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_name.htm` |
| Number of Events | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_DataAuditTrail_numOfEvents.htm` |
| Operation | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_operation.htm` |
| Operator | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_operator.htm` |
| Select Event | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_SelectEvent.htm` |
| Date/Time | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_time.htm` |
| Type | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_type.htm` |
| Object Version | Data Audit Trail Variables | `ReportVariables_CSH/RepVar_DataAuditTrail_version.htm` |

### FractionDetParam

**Official Help topics:** 18

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Fraction Detection Parameter Category | The Fraction Detection Parameter includes variables that give information about the defined detection parameters used to detect the peaks within a fraction for peak-based fractionation. They can be defined in the = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/GLOSSARY_INSTRUM | `ReportVariables_CSH/RepVar_FractionDetParam.htm` |
| Baseline Drift | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_baselineDrift.htm` |
| Baseline Offset | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_baselineOffset.htm` |
| Detection Channel | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_channel.htm` |
| Deriv. Step | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_derivStep.htm` |
| Peak End Curve | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_endCurve.htm` |
| Peak End Slope | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_endSlope.htm` |
| Peak End Threshold | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_endThreshold.htm` |
| Peak End True Time | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_endTrueTime.htm` |
| Peak Max Slope | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_maxSlope.htm` |
| Peak Max True Time | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_maxTrueTime.htm` |
| Channel Name | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_name.htm` |
| Peak Start Curve | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_startCurve.htm` |
| Peak Start Slope | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_startSlope.htm` |
| Peak Start Threshold | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_startThreshold.htm` |
| Peak Start True Time | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_startTrueTime.htm` |
| Threshold No Peak End | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_thresholdNoPeakEnd.htm` |
| Threshold Do Not Resolve | Fraction Detection Parameter Variable | `ReportVariables_CSH/RepVar_FractionDetParam_thrshldNoResolve.htm` |

### MassSpectrum

**Official Help topics:** 17

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Mass Spectrum Category | The variables in the Mass Spectrum category report information about the mass spectrum specified in the Parameters dialog box of the respective variable (see Mass Spectrum (Chromatogram Variable) , Mass Spectrum (Mass Spectrometry Variable) , and Peak Mass Spectrum (Peak Purity/Identification Variable) . The following table lists the available variables in t | `ReportVariables_CSH/RepVar_MassSpectrum.htm` |
| Baseline | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_baseline.htm` |
| Detected Mass Accuracies | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_detected_mass_accuracies.htm` |
| Detected Masses | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_detected_masses.htm` |
| FT Resolution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_ftresolution.htm` |
| Number of Data Points | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_count.htm` |
| Mass Detected | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_detected.htm` |
| Mass Detected Formulas | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_detected_formulas.htm` |
| Maximal Mass | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_max.htm` |
| Minimal Mass | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_min.htm` |
| Mass Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_mass_range.htm` |
| Noise | Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_MassSpectrum_noise.htm` |
| Relative Intensity | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_rel_intensity.htm` |
| Resolution | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_resolution.htm` |
| Signal to Noise | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_signal_to_noise.htm` |
| TIC | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_TIC.htm` |
| Spectrum Type | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_MassSpectrum_type.htm` |

### SSTDefinition

**Official Help topics:** 17

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Test Case Category | The Test Case category includes variables that give information about the conditions defined for a specific test case. The following table lists the available variables in this category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_SSTDefinition.htm` |
| Channel | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_channel.htm` |
| Evaluation Formula | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_eval_formula.htm` |
| Injection Condition | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_injection_condition.htm` |
| Fail Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_fail_action_list.htm` |
| Number of Fail Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_number_fail_actions.htm` |
| Number of Pass Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_number_pass_actions.htm` |
| Pass Actions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_irc_pass_action_list.htm` |
| Name | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_name.htm` |
| Incomputable Interpretation (N.A.) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_not_available.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_number.htm` |
| Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_operator.htm` |
| Peak Specification | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_peak_condition.htm` |
| Reference Value Formula | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_reference_value.htm` |
| Number of Decimal Places | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_round_digits.htm` |
| Statistics | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_statistics.htm` |
| Minimum/Maximum Number of Injections | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTDefinition_statistics_min_injections.htm` |

### CM6History

**Official Help topics:** 14

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Chromeleon 6 History Category | The Chromeleon 6 History category includes variables that give information about the Chromeleon 6 history. It is only available in the context of the Chromeleon 6 History Report Table. The following table lists the available variables in the Chromeleon 6 History category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_CM6History.htm` |
| Comment | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_comment.htm` |
| Detail Column | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_column.htm` |
| Detail Comment | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_comment.htm` |
| Detail New Value | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_new_value.htm` |
| Detail Number | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_number.htm` |
| Detail Object | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_object.htm` |
| Detail Old Value | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_detail_old_value.htm` |
| Object Name | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_name.htm` |
| Operation | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_operation.htm` |
| Operator | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_operator.htm` |
| Object Path | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_path.htm` |
| Date/Time | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_time.htm` |
| Object Version | Report Variables—Chromeleon 6 History | `ReportVariables_CSH/RepVar_CM6History_version.htm` |

### GlobalFunctions

**Official Help topics:** 14

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Global Functions Category | The Global Functions category includes global functions that are similar to the related functions in Microsoft Excel. The following table lists the available functions in the Global Functions category. Click a function name to read the full description. The functions are also available outside this category. | `ReportVariables_CSH/RepVar_GlobalFunctions.htm` |
| Absolute Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_abs.htm` |
| Exponential Function | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_exp.htm` |
| Find Position of Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_find.htm` |
| If | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_if.htm` |
| Is Error | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_iserror.htm` |
| Select Left Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_left.htm` |
| Natural Logarithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_ln.htm` |
| Logarithm | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_log.htm` |
| Select Middle Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_mid.htm` |
| Select Right Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_right.htm` |
| Round Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_round.htm` |
| Convert to Text | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_text.htm` |
| Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_GlobalFunctions_time.htm` |

### Fraction

**Official Help topics:** 12

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Fraction Category | The Fraction category includes variables that give information about the fraction, a group of tubes, in a tray collected during a sequence run. This is referred to as 'fraction collection'. Depending on whether time-based or peak-based fractionation has been used, a value is reported for the fraction defined by the corresponding detection channel settings fo | `ReportVariables_CSH/RepVar_Fraction.htm` |
| Channel Parameter | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_channel.htm` |
| End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_endTime.htm` |
| Number of Peaks | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_nPeaks.htm` |
| Number of Tubes | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_nTubes.htm` |
| Number | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_number.htm` |
| Select Peak | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_peak.htm` |
| Start Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_startTime.htm` |
| Select Tube | Open the Report Column dialog box (for example, by double-clicking a column header in the Interactive Results Table or other report table). | `ReportVariables_CSH/RepVar_Fraction_tube.htm` |
| Tube Positions | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_tubePosition.htm` |
| Tube Position Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_tubePositionRange.htm` |
| Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Fraction_volume.htm` |

### Peptide

**Official Help topics:** 12

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Peptide Category | The following table lists the available variables in the Peptide category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peptide.htm` |
| Charge | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_charge.htm` |
| Isotope | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_isotope.htm` |
| Isotope excluded? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Peptide_isotope_isExcluded.htm` |
| Peptide Isotope Category | The following table lists the available variables in the Peptide Isotope category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_Peptide_Isotope_Params.htm` |
| Simulated Abundance | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_Peptide_Isotope_simulatedAbundance.htm` |
| Simulated Mass | MS Extraction Parameters Variable | `ReportVariables_CSH/RepVar_Peptide_Isotope_simulatedMass.htm` |
| Number of Isotopes in Observed Isotopic Distribution | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_numberRealIsoDistrib.htm` |
| Number of Isotopes in Theoretical Isotopic Distribution | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_numberSimIsoDistrib.htm` |
| Number of Charge States | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_numChargeStates.htm` |
| Observed Isotopic Distribution | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_realIsoDistrib.htm` |
| Theoretical Isotopic Distribution | Open the Report Column dialog box of the peptide table (for example, by double-clicking a column header in the peptide table). | `ReportVariables_CSH/RepVar_Peptide_simIsoDistrib.htm` |

### General

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| General Category | The General category includes variables that give information about the computer, Chromeleon, or the user. The following table lists the available variables in the General category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_General.htm` |
| Computer Name | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_computerName.htm` |
| Current Printer | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_currentPrinter.htm` |
| Current Time | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_currentTime.htm` |
| Logged on User | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_loggedOnUser.htm` |
| My Documents Folder | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_mydocumentsfolder.htm` |
| Report Mode | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportMode.htm` |
| Report Operator | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportOperator.htm` |
| Report Time | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_reportTime.htm` |
| Serial Number | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_serialNo.htm` |
| Version Number | In the Report Designer, right-click a cell and select Insert > Report Variables to insert a variable, or select Report Formula Properties to modify one. The Formula Properties Report dialog opens. –OR– If creating or modifying a report table column in the Report Designer or in Interactive Results, double-click the column (or select Column Properties from the | `ReportVariables_CSH/RepVar_General_version.htm` |

### InstrumentMethod

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Instrument Method Category | The Instrument Method category includes variables that give information about the instrument method. The following table lists the available variables in the Instrument Method category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_InstrumentMethod.htm` |
| Comment | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_comment.htm` |
| Creation Operator | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_creation_operator.htm` |
| Creation Date & Time | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_creation_time.htm` |
| Data Vault | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_dataVault.htm` |
| Directory | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_directory.htm` |
| Instrument | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_instrument.htm` |
| Name | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_name.htm` |
| Server | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_server.htm` |
| Last Update Operator | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_update_operator.htm` |
| Last Update Date & Time | Instrument Method Variable | `ReportVariables_CSH/RepVar_InstrumentMethod_update_time.htm` |

### MassSpectrometry

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Mass Spectrometry Category | The Mass Spectrometry category includes variables that give information about the mass spectrometry instrument status and setting. The following table lists the available variables in the Mass Spectrometry category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_MassSpectrometry.htm` |
| Device Information Category | Open the Device Information category by selecting the Device Information variable of the Mass Spectrometry Category . The variables in the Device Information category report information about the used MS device . The following table lists the available variables in the category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_MassSpectrometry_device.htm` |
| Device Name | Device Information Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_device_deviceName.htm` |
| Firmware Version | Device Information Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_device_firmwareVersion.htm` |
| Hardware Version | Device Information Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_device_hardwareVersion.htm` |
| Model | Device Information Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_device_model.htm` |
| Name | Device Information Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_device_name.htm` |
| Spectra Count | Mass Spectrometry Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_spec_count.htm` |
| Mass Spectrum Parameters | Mass Spectrometry Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_spectrum.htm` |
| Status Log | Mass Spectrometry Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_statusLog.htm` |
| Tune Data | Mass Spectrometry Variable | `ReportVariables_CSH/RepVar_MassSpectrometry_tune.htm` |

### ReportTemplate

**Official Help topics:** 11

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Report Template | The Report Template category includes variables that give information about the report template used. It is only available in the Report Designer (not in report tables). The following table lists the available variables in the Report Template category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_ReportTemplate.htm` |
| Creation Operator | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_creation_operator.htm` |
| Creation Date & Time | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_creation_time.htm` |
| Current Sheet Name | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_curSheetName.htm` |
| Current Sheet Number | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_curSheetNo.htm` |
| Data Vault | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_dataVault.htm` |
| Directory | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_directory.htm` |
| Name | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_name.htm` |
| Number of Sheets | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_sheets.htm` |
| Last Update Operator | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_update_operator.htm` |
| Last Update Date & Time | In the Report Designer , right-click an empty cell. | `ReportVariables_CSH/RepVar_ReportTemplate_update_time.htm` |

### ReportValueList

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Statistics Category | Open the Statistics category by selecting the Statistics variable of the Test Case Result category. The variables in the Statistics category return the result of a statistics function used to calculate the evaluation formula (system suitability test case only). | `ReportVariables_CSH/RepVar_ReportValueList.htm` |
| Average | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_average.htm` |
| Count | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_count.htm` |
| Minimum/Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_minimum.htm` |
| Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_range.htm` |
| Relative Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_rel_range.htm` |
| Relative Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_rel_stddev.htm` |
| Standard Deviation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_stdev.htm` |
| Sum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_ReportValueList_sum.htm` |

### SLS

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Spectra Library Screening Category | Open the Spectra Library Screening category by selecting the Spectra Library Screening Parameters variable of the Processing Method category. The variables in the Spectra Library Screening category give information about the settings selected on the Spectral Library Screening dialog box of the Processing Method Editor. The following table lists the available | `ReportVariables_CSH/RepVar_SLS.htm` |
| Spectrum Derivative | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_derivative.htm` |
| Library Spectral Filter | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_filter.htm` |
| Is Library Spectral Filter Active | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_is_filter_active.htm` |
| Is Spectra Library Used | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_is_library_used.htm` |
| Spectra Library / Folder | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_library.htm` |
| Match Criterion | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_match.htm` |
| Hit Threshold | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_threshold.htm` |
| Wavelength Range Minimum/Maximum | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_SLS_wavelength_max.htm` |

### SSTResults

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Test Case Result Category | The Test Case Result category includes variables that give information about the results of a specific test case. The following table lists the available variables in this category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_SSTResults.htm` |
| Evaluation Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_eval_result.htm` |
| Injection Evaluation Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_injection_eval_result.htm` |
| Injection Condition Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_injection_match.htm` |
| Message | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_message.htm` |
| Peak Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_peak_result.htm` |
| Reference Value | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_reference_value.htm` |
| Result | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_result.htm` |
| Statistics | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SSTResults_statistics.htm` |

### Table

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Group Average | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupaverage.htm` |
| Group Count | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupcount.htm` |
| Group Maximum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupmax.htm` |
| Group Minimum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupmin.htm` |
| Group Range | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprange.htm` |
| Group Relative Range | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprelrange.htm` |
| Group Relative Standard Deviation | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_grouprelstdev.htm` |
| Group Standard Deviation | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupstdev.htm` |
| Group Sum | Integration/Summary Table Variable | `ReportVariables_CSH/RepVar_Table_groupsum.htm` |

### UvSettings

**Official Help topics:** 9

| Variable / topic | Help summary | Help topic |
|---|---|---|
| UV Settings Category | Open the UV Settings category by selecting the UV Spectra Settings variable of the Processing Method category. The variables in the UV Settings category give information about the settings selected on the UV Spectra Settings and UV Spectra Comparison Defaults dialog boxes of the Processing Method Editor. The following table lists the available variables in t | `ReportVariables_CSH/RepVar_UvSettings.htm` |
| Baseline Correction | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_baseline_correction.htm` |
| Spectrum Derivative | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_derivative.htm` |
| Minimum/Maximum of Fixed Baseline Correction Range | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_fixed_blcorrection_range_max.htm` |
| Left/Right Region Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_left_region_bunch.htm` |
| Match Criterion | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_match.htm` |
| Peak Spectrum Bunch | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_peak_spectrum_bunch.htm` |
| Peak Purity Threshold | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_threshold.htm` |
| Wavelength Range Minimum/Maximum | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_UvSettings_wavelength_max.htm` |

### FractionTube

**Official Help topics:** 8

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Fraction Tube Category | The Fraction Tube includes variables that give information about a specific tube. The following table lists the available variables in this category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_FractionTube.htm` |
| End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_endTime.htm` |
| Maximum Collectable Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_maxVolume.htm` |
| Number of Peaks | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_nPeaks.htm` |
| Select Peak | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_peak.htm` |
| Tube Position | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_position.htm` |
| Start Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_startTime.htm` |
| Collected Volume | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_FractionTube_volume.htm` |

### RefMsSettings

**Official Help topics:** 8

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Reference Mass Spectrum Settings Category | Open the Reference Mass Spectrum Settings category by selecting the Reference Mass Spectrum variable of the Component Category . The variables in the Reference Mass Spectrum Settings category report information about the settings selected in the Reference Mass Spectrum Settings dialog box of the Processing Method Editor. The following table lists the availab | `ReportVariables_CSH/RepVar_RefMsSettings.htm` |
| Auto Filter | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_filter.htm` |
| Match Threshold | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_matchThreshold.htm` |
| Mol. Weight | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_molWeight.htm` |
| Reverse Match Threshold | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_reverseMatchThreshold.htm` |
| Reverse Search | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_reverseSearch.htm` |
| Search Type | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_searchType.htm` |
| Search with Mol. Weight | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSettings_searchWithMolWeight.htm` |

### MsSigExtractionParams

**Official Help topics:** 7

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Auto Filter | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_autoFilter.htm` |
| End Time | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_endTime.htm` |
| Mass Ranges | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_massRanges.htm` |
| Number of Smoothing Points | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_nSmoothingPoints.htm` |
| Smoothing Algorithm | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_smoothingAlgorithm.htm` |
| Start Time | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_startTime.htm` |
| Trace Type | MS Signal Extraction Parameters Variable | `ReportVariables_CSH/RepVar_MsSigExtractionParams_traceType.htm` |

### Version

**Official Help topics:** 7

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Version Category | The Version category includes variables that retrieve information about the current version of an object (sequence, injection, chromatogram, instrument method, processing method, report template or library spectrum). | `ReportVariables_CSH/RepVar_Version.htm` |
| Comment | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_comment.htm` |
| Computer Name | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_computerName.htm` |
| Data Vault | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_dataVault.htm` |
| Number | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_number.htm` |
| Operator | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_operator.htm` |
| Date & Time | In the Report Designer, click in the cell in which you want to insert a variable. | `ReportVariables_CSH/RepVar_Version_Time.htm` |

### AuditTrailEvent

**Official Help topics:** 6

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Description | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_description.htm` |
| Object Name | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_name.htm` |
| Operator | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_operator.htm` |
| Role | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_role.htm` |
| Date/Time | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_time.htm` |
| Event Type | Audit Trail Event Variables | `ReportVariables_CSH/RepVar_AuditTrailEvent_type.htm` |

### eWorkflow

**Official Help topics:** 6

| Variable / topic | Help summary | Help topic |
|---|---|---|
| eWorkflow Category | The eWorkflow category includes variables that give information about the eWorkflow used to create a sequence. The category is only available in the eWorkflow Editor when defining templates for sequences. The following table lists the available variables in the eWorkflow category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_eWorkflow.htm` |
| Description | On the Create menu in the Chromeleon Console, click eWorkflow . | `ReportVariables_CSH/RepVar_eWorkflow_description.htm` |
| Instrument Used | On the Create menu in the Chromeleon Console, click eWorkflow . | `ReportVariables_CSH/RepVar_eWorkflow_instrument_used.htm` |
| Name | On the Create menu in the Chromeleon Console, click eWorkflow . | `ReportVariables_CSH/RepVar_eWorkflow_name.htm` |
| State | On the Create menu in the Chromeleon Console, click eWorkflow . | `ReportVariables_CSH/RepVar_eWorkflow_state.htm` |
| Type | On the Create menu in the Chromeleon Console, click eWorkflow . | `ReportVariables_CSH/RepVar_eWorkflow_type.htm` |

### TimeFunctions

**Official Help topics:** 5

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions.htm` |
| Format Date & Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_format.htm` |
| Local Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_local.htm` |
| Time Offset | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_offset.htm` |
| Coordinated Universal Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_TimeFunctions_utc.htm` |

### Imported

**Official Help topics:** 3

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Peak Calibration (Imported) Category | The Peak Calibration (Imported) category is only available for sequences containing imported non-Chromeleon data. It contains report variables for all original imported data values that give information about the calibration values and settings. | `ReportVariables_CSH/RepVar_Imported_Peak_Calibration.htm` |
| Peak Purity and Identification (Imported) Category | The Peak Purity and Identification (Imported) category is only available for sequences containing imported non-Chromeleon data. It contains report variables for all original imported data values that give information about the comparison of peak spectra with reference spectra. These report variables will only work if a 3D field is available for the current i | `ReportVariables_CSH/RepVar_Imported_Peak_PurityAndId.htm` |
| Peak Results (Imported) Category | The Peak Results (Imported) category is only available for sequences containing imported non-Chromeleon data. It contains report variables for all original imported data values that give information about peak results. | `ReportVariables_CSH/RepVar_Imported_Peak_Results.htm` |

### PeakGroup

**Official Help topics:** 3

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Peak Group | The Peak Group category includes variables that give information about the values in the Peak Group Table of the processing method. The following table lists the available variables in the Peak Group category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_PeakGroup.htm` |
| Group Evaluation | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_PeakGroup_group_evaluation.htm` |
| Start/End Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_PeakGroup_StartEndTime.htm` |

### SpecLib

**Official Help topics:** 3

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Library Record Category | Open the Library Record category, for example, by selecting the Library Record variable of the Hit Spectrum category. It includes variables that retrieve information about the = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/Glossary_Spectral_Library.htm');return false;">Spectr | `ReportVariables_CSH/RepVar_SpecLib.htm` |
| Creation Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SpecLib_creation_operator.htm` |
| Last Update Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_SpecLib_update_operator.htm` |

### FormulaEditor

**Official Help topics:** 2

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Insert Formula | This dialog box opens, for example, in the chromatogram properties: | `ReportVariables_CSH/RepVar_FormulaEditor_Full.htm` |
| Report Formula Editor | In the Chromeleon Studio, navigate into the Report Designer category. | `ReportVariables_CSH/RepVar_FormulaEditor_Reduced.htm` |

### Manual

**Official Help topics:** 2

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Injection Specific XIC Detection Operator | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Manual_Detection_Operator.htm` |
| Injection Specific XIC Detection Time | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Manual_Detection_Time.htm` |

### AuditTrail

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Audit Trail Category | The Audit Trail category includes variables that give information about all events that are logged in the Injection = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/GLOSSARY_AUDIT_TRAIL.htm');return false;">Audit Trail . The available variables depend on the installed system an | `ReportVariables_CSH/RepVar_AuditTrail.htm` |

### AuditTrailEvents

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Audit Trail Event Category | Variables of the audit trail event report category are used in the Audit Trail Event report table . Below is a list of available variables in the Audit Trail Event category. Click a variable name to read the full description. | `ReportVariables_CSH/RepVar_AuditTrailEvents.htm` |

### CellFormula

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Formula | Report Variable Properties Dialog | `ReportVariables_CSH/RepVar_CellFormula.htm` |

### CompositeScoringCategory

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Composite Scoring Categories | Peak Purity and Identification / Processing Method Report Variables | `ReportVariables_CSH/RepVar_CompositeScoringCategory.htm` |

### CustomFormulas

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Custom Formulas Category | The Custom Formulas category lets you evaluate your own bespoke expressions created using the Custom Formula Wizard . | `ReportVariables_CSH/RepVar_CustomFormulas.htm` |

### CustomVar

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Custom Variable | Component/Injection/Sequence/Peak Group Variable | `ReportVariables_CSH/RepVar_CustomVar.htm` |

### Evaluate

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Evaluate | Chromatogram/Injection/Peak Result Variable | `ReportVariables_CSH/RepVar_Evaluate.htm` |

### IntegrationTable

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Integration Table and Summary Table Categories | Note: On the Summary tab page, the Summary Table category is available. On all other tab pages, the Integration Table category is available. | `ReportVariables_CSH/RepVar_IntegrationTable_SummaryTable.htm` |

### Manually

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Injection Specific XIC Detection? | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/RepVar_Manually_Detected.htm` |

### Precondition

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Preconditions Category | The Preconditions category includes variables that give information about the instrument settings that were logged in the Injection = 4 && typeof(BSPSPopupOnMouseOver) == 'function') BSPSPopupOnMouseOver(event);" class="BSSCPopup" onclick="BSSCPopup('../Glossary/GLOSSARY_AUDIT_TRAIL.htm');return false;">Audit Trail before the analysis. The available variable | `ReportVariables_CSH/RepVar_Precondition.htm` |

### RefMsSetting

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Reference Mass Spectrum | Reference Mass Spectrum Settings Variable | `ReportVariables_CSH/RepVar_RefMsSetting_spectrum.htm` |

### repvar

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Height (Peak Height) | Open the Report Column dialog box (for example, by double-clicking a column header in a report table). | `ReportVariables_CSH/repvar_peak_results_height.htm` |

### sls

**Official Help topics:** 1

| Variable / topic | Help summary | Help topic |
|---|---|---|
| Number of Spectra Libraries / Folders | Spectra Library Screening Variable | `ReportVariables_CSH/RepVar_sls_library_count.htm` |

## Authoring Rule

1. Select the formula engine first: direct CM report formula or FormulaOne workbook formula.
2. For direct CM formulas, select an observed device path/channel/component from the carrier or configuration KB.
3. For FormulaOne, use a documented function and an existing target cell; preserve workbook structure.
4. If the carrier/configuration does not prove the variable path or function behaviour, mark `OPEN VERIFICATION REQUIRED`.
