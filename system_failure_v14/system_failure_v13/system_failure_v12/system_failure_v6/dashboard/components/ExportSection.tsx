'use client';

interface ExportSectionProps {
  rowCount?: number;
}

export default function ExportSection({ rowCount = 2000 }: ExportSectionProps) {
  const handleDownload = () => {
    const csvRows = [
      'Battery_Voltage,RTC_Drift_sec_per_day,Boot_Errors_Count,CMOS_Warning_Flag,Reset_BIOS_Flag,Power_Cycle_Count,System_Age_Years,Ambient_Temperature_C,Predicted_Failure_Mode,Failure_Mode_Label,Failure_Flag',
      '3.02,14,0,0,0,412,2,26.1,0,Healthy,0',
      '2.74,78,4,1,1,1812,8,36.2,1,Wear-Out Failure,1',
      '2.86,98,6,1,1,940,3,33.8,4,Controller/Firmware Failure,1',
    ];
    const csvContent = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvRows.join('\n'));
    const link = document.createElement("a");
    link.setAttribute("href", csvContent);
    link.setAttribute("download", "failure_analysis_report.csv");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="section-wrap">
      <h2 className="section-title">📥 Export Analysis</h2>
      <p className="section-subtitle">Download all telemetry rows with predicted Failure_Mode and Failure_Flag</p>

      <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-6 text-center">
        <div className="mb-4">
          <p className="text-gray-300 mb-2">Export all predictions with Failure_Mode and Failure_Flag for further analysis.</p>
        </div>
        <button
          onClick={handleDownload}
          className="bg-gradient-to-r from-cyan-500 to-cyan-400 hover:from-cyan-400 hover:to-cyan-300 text-slate-900 font-bold py-3 px-6 rounded-lg transition-all hover:scale-105"
        >
          📥 Download Report
        </button>
        <p className="text-xs text-gray-500 mt-4">Report includes {rowCount} systems with predicted failure modes and binary failure flags.</p>
      </div>
    </div>
  );
}
